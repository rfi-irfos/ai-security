import yaml
import os
from litellm import completion
import litellm
from dotenv import load_dotenv

load_dotenv()
litellm._turn_on_debug()

class LLMService:
    def __init__(self, config_path="config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        
        self.models = {m["name"]: m for m in self.config.get("models", [])}
        self.default_model = self.config.get("default_model")

    def get_available_models(self):
        return [m["name"] for m in self.config.get("models", [])]

    def generate_response(self, messages, model_name=None, tools=None):
        if not model_name:
            model_name = self.default_model
        
        model_config = self.models.get(model_name)
        if not model_config:
            raise ValueError(f"Model {model_name} not found in configuration.")

        model_id = model_config["model_id"]
        # Check for OpenAI Compatible endpoint override
        api_base = model_config.get("api_base")
        
        kwargs = {
            "model": model_id,
            "messages": messages,
        }
        
        if api_base:
            kwargs["api_base"] = api_base
        if tools:
            kwargs["tools"] = tools

        try:
            response = completion(**kwargs)
            message = response.choices[0].message

            # If we are using tools, we need to return the raw message object to handle tool_calls
            if tools is not None:
                return message

            content = message.content
            if content is None:
                return "Error: Content blocked by LLM provider safety filters."
            return content
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"
