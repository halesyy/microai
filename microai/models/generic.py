
from typing import Literal
from pydantic import BaseModel

MessageRoles = Literal["system", "user", "assistant"]

class Message(BaseModel):
   content: str | None
   role: MessageRoles
   name: str | None = None

def user_message(content: str):
   return Message(role="user", content=content)