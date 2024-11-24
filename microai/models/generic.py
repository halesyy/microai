
from typing import Literal
from pydantic import BaseModel

class Message(BaseModel):
   content: str
   role: Literal["system", "user", "assistant"]
   name: str | None = None

def user_message(content: str):
   return Message(role="user", content=content)