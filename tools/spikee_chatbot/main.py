import os
import uuid
import datetime
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from fastapi.staticfiles import StaticFiles
from llm_service import LLMService
from guardrails import check_guardrails
import json
from prompts import SYSTEM_PROMPTS
from tools import API_TOOLS, SQL_TOOLS, TOOLS_MAP

app = FastAPI()

# Database Setup
DATABASE_URL = "sqlite:///./chat.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChatSession(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("sessions.id"))
    role = Column(String)  # "user" or "assistant"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    session = relationship("ChatSession", back_populates="messages")

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Services
llm_service = LLMService()

# Pydantic Models
class MessageRequest(BaseModel):
    session_id: str | None = None
    message: str
    model: str | None = None
    guardrail: str | None = "off"
    system_prompt: str | None = None
    llm_judge_config: dict | None = None
    tool_mode: str | None = "None"

class ToolTraceItem(BaseModel):
    tool_name: str
    args: dict
    result: str

class MessageResponse(BaseModel):
    session_id: str
    response: str
    model_used: str
    tool_traces: list[ToolTraceItem] = []

class ModelListResponse(BaseModel):
    models: list[str]
    default_model: str

class SessionListItem(BaseModel):
    id: str
    preview: str
    created_at: datetime.datetime

class HistoryListResponse(BaseModel):
    sessions: list[SessionListItem]

class ChatMessageItem(BaseModel):
    role: str
    content: str

class SessionDetailResponse(BaseModel):
    session_id: str
    messages: list[ChatMessageItem]

class PromptsListResponse(BaseModel):
    prompts: list[str]

# API API Endpoints
@app.get("/api/prompts", response_model=PromptsListResponse)
def get_prompts():
    return {"prompts": list(SYSTEM_PROMPTS.keys())}

@app.get("/api/prompts/{name}")
def get_prompt(name: str):
    if name in SYSTEM_PROMPTS:
        return {"prompt": SYSTEM_PROMPTS[name]}
    raise HTTPException(status_code=404, detail="Prompt not found")

@app.get("/api/sessions", response_model=HistoryListResponse)
def list_sessions(db: Session = Depends(get_db)):
    # Get sessions ordered by creation date desc
    sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()
    result = []
    for s in sessions:
        # Get first user message as preview
        first_msg = db.query(ChatMessage).filter(ChatMessage.session_id == s.id, ChatMessage.role == "user").order_by(ChatMessage.created_at).first()
        preview = first_msg.content[:50] + "..." if first_msg else "New Session"
        result.append(SessionListItem(id=s.id, preview=preview, created_at=s.created_at))
    return {"sessions": result}

@app.get("/api/sessions/{session_id}", response_model=SessionDetailResponse)
def get_session_history(session_id: str, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    msgs = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()
    return {
        "session_id": session_id,
        "messages": [{"role": m.role, "content": m.content} for m in msgs]
    }

@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Cascade delete messages (or rely on SQL cascade if setup, but here manual is safer for SQLite basic setup)
    db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
    db.delete(session)
    db.commit()
    return {"status": "deleted"}

@app.delete("/api/sessions")
def delete_all_sessions(db: Session = Depends(get_db)):
    db.query(ChatMessage).delete()
    db.query(ChatSession).delete()
    db.commit()
    return {"status": "deleted all"}

@app.get("/api/models", response_model=ModelListResponse)
def list_models():
    return {
        "models": llm_service.get_available_models(),
        "default_model": llm_service.default_model
    }

@app.post("/api/chat", response_model=MessageResponse)
def chat_endpoint(req: MessageRequest, db: Session = Depends(get_db)):
    session_id = req.session_id
    
    # 1. Guardrails Check
    is_blocked = check_guardrails(req.message, req.guardrail, llm_service, req.llm_judge_config)
    
    # Check if session exists or create new
    is_new_session = False
    if session_id:
        chat_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not chat_session:
            chat_session = ChatSession(id=session_id)
            db.add(chat_session)
            db.commit()
            is_new_session = True
    else:
        session_id = str(uuid.uuid4())
        chat_session = ChatSession(id=session_id)
        db.add(chat_session)
        db.commit()
        is_new_session = True

    # If new session AND a system prompt is provided, save it as a system message
    if is_new_session and req.system_prompt:
        system_msg = ChatMessage(session_id=session_id, role="system", content=req.system_prompt)
        db.add(system_msg)
        db.commit()

    # Save User Message
    user_msg = ChatMessage(session_id=session_id, role="user", content=req.message)
    db.add(user_msg)
    db.commit()

    # If blocked, abort generation and save a canned refusal
    if is_blocked:
        response_text = f"Blocked by guardrail: {req.guardrail}"
        agent_msg = ChatMessage(session_id=session_id, role="assistant", content=response_text)
        db.add(agent_msg)
        db.commit()
        
        return {
            "session_id": session_id,
            "response": response_text,
            "model_used": "guardrails-blocker"
        }

    # Prepare context for LLM
    # We load all messages for context. For production, apply sliding window or limit.
    history_msgs = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()
    llm_messages = [{"role": m.role, "content": m.content} for m in history_msgs]

    tools_list = None
    if req.tool_mode == "API Mode":
        tools_list = API_TOOLS
    elif req.tool_mode == "SQL Mode":
        tools_list = SQL_TOOLS

    tool_traces = []

    MAX_TURNS = 5
    for turn in range(MAX_TURNS):
        # Generate Response
        try:
            response_msg = llm_service.generate_response(llm_messages, model_name=req.model, tools=tools_list)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        if tools_list is None:
            # response_msg is just a string when tools=None
            content = response_msg
            tool_calls = None
        else:
            # Litellm might return string on error
            if isinstance(response_msg, str):
                content = response_msg
                tool_calls = None
            else:
                content = response_msg.content
                tool_calls = getattr(response_msg, "tool_calls", None)

        # Keep context up to date for next loop
        msg_dict = {"role": "assistant", "content": content or ""}
        if tool_calls:
            msg_dict["tool_calls"] = [tc.model_dump() if hasattr(tc, 'model_dump') else dict(tc) for tc in tool_calls]
        llm_messages.append(msg_dict)

        if not tool_calls:
            # Save final Assistant Response
            agent_msg = ChatMessage(session_id=session_id, role="assistant", content=content or "")
            db.add(agent_msg)
            db.commit()

            return {
                "session_id": session_id,
                "response": content or "",
                "model_used": req.model or llm_service.default_model,
                "tool_traces": tool_traces
            }

        # Execute tools
        for tool_call in tool_calls:
            try:
                func_name = tool_call.function.name
                raw_args = tool_call.function.arguments
                args = json.loads(raw_args)
                if not isinstance(args, dict):
                    raise ValueError("Tool arguments must be a JSON object.")
            except (AttributeError, TypeError, ValueError, json.JSONDecodeError) as e:
                func_name = getattr(getattr(tool_call, "function", None), "name", None) or "unknown_tool"
                args = {}
                result = f"Error: Invalid arguments for tool {func_name}: {e}"
            else:
                tool_function = TOOLS_MAP.get(func_name)
                if not tool_function:
                    result = f"Error: Unknown tool {func_name}"
                else:
                    try:
                        result = tool_function(**args)
                    except Exception as e:
                        result = f"Error executing tool {func_name}: {e}"

            result_str = str(result)

            # Create tool message for LLM
            tool_msg = {
                "role": "tool",
                "name": func_name,
                "content": result_str,
                "tool_call_id": getattr(tool_call, "id", ""),
            }
            llm_messages.append(tool_msg)

            # Collect trace for the frontend
            tool_traces.append({"tool_name": func_name, "args": args, "result": result_str})

    return {
        "session_id": session_id,
        "response": "Error: Maximum tool execution turns reached.",
        "model_used": req.model or llm_service.default_model,
        "tool_traces": tool_traces
    }

# Serve Static Files (Frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
