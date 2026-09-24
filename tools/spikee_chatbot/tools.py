import json
import mock_bank_db

# Hardcoded current user ID to simulate authentication context
CURRENT_USER_ID = 123

def get_current_user():
    """Returns the current logged in user details."""
    user = mock_bank_db.get_user(CURRENT_USER_ID)
    return json.dumps(user) if user else json.dumps({"error": "User not found"})

def get_user_account(user_id: int):
    """Returns the account details for the given user_id."""
    accounts = mock_bank_db.get_user_accounts(user_id)
    return json.dumps(accounts)

def get_user_transactions(user_id: int):
    """Returns a JSON list of user transactions for the given user_id."""
    transactions = mock_bank_db.get_user_transactions(user_id)
    return json.dumps(transactions)

def execute_sql_query(query: str):
    """Executes a raw SQLite query against the database. Returns the results as a JSON string."""
    query = str(query).replace("`", "").replace("sql", "").strip()
    result = mock_bank_db.execute_sql(query)
    return json.dumps(result, indent=2, default=str)

# Mapping of tool names to their actual Python functions
TOOLS_MAP = {
    "get_current_user": get_current_user,
    "get_user_account": get_user_account,
    "get_user_transactions": get_user_transactions,
    "execute_sql_query": execute_sql_query
}

# Definitions to pass to LiteLLM / OpenAI API format
API_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_user",
            "description": "Returns the current logged in user details."
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_account",
            "description": "Returns the account details for the given user_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user."
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_transactions",
            "description": "Returns a JSON list of user transactions for the given user_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user."
                    }
                },
                "required": ["user_id"]
            }
        }
    }
]

SQL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_sql_query",
            "description": "Executes a raw SQLite query against the database. Returns the results as a JSON string. The schema has users(id, name, email), accounts(id, user_id, account_type, balance), transactions(id, user_id, amount, type, description, date).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQLite query to execute."
                    }
                },
                "required": ["query"]
            }
        }
    }
]
