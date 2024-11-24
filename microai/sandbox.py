
import json
from typing import Any, Callable, Literal

from openai import BaseModel
from microai.models.chatgpt import chat_message
from microai.models.generic import Message, user_message
from openai.types.chat_model import ChatModel

def code(work: str, model: ChatModel = "gpt-3.5-turbo"):
   messages: list[Any | Message] = []
   messages.append(Message(
      content="You are an opinionated programmer who will receive tasks to complete. Structured and stylistically consistent code development. You follow these coding principles: function-biased over classes, repository pattern, and ensures alignment with the following tech stack: Frontend - React, NextJS, NextUI, TailwindCSS, Firebase, and Firebase Auth; Backend - Python 3.12 with pydantic for data classes and database objects.",
      role="system"
   ))
   messages.append(Message(
      content=f"Start by planning out the following work, with no coding: {work}",
      role="user"
   ))
   messages.append(chat_message(messages, model=model))
   messages.append(Message(
      content="Now consider possible side-effects, and correct usage of frameworks.",
      role="user"
   ))
   messages.append(chat_message(messages, model=model))
   messages.append(Message(
      content="Now produce the directory structure expected to be modified.",
      role="user"
   ))
   messages.append(chat_message(messages, model=model))
   messages.append(Message(
      content="Now produce only the directory structure expected to be modified.",
      role="user"
   ))
   messages.append(chat_message(messages, model=model))
   messages.append(Message(
      content="Now code the features.",
      role="user"
   ))
   messages.append(chat_message(messages, model=model))
   history = [m.model_dump() for m in messages]
   open("history.json", "w").write(json.dumps(history, indent=4))

def coder(
   language: str = "python 3.12",
   framework: str | None = None,
   mode: Literal["writing", "refactoring", "bug-finding"] = "writing",
   context_file: str | None = None
):
   pass

class Node(BaseModel):
   type: Literal["start", "task", "end"] = "task"
   func: Callable
   description: str | None = None

nodes = [

]

def main():
   # code("make a store onboarding page in pages/onboarding/store.tsx, use NextUI for styling to make it look nice")
   m = chat_message([user_message("Hello")])
   print(m)

if __name__ == "__main__":
   main()