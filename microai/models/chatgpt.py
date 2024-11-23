
import logging
import os
from typing import Any, Literal, TypedDict

from dotenv import load_dotenv
from openai import OpenAI

from microai.models.generic import Message
from openai.types.chat_model import ChatModel
from openai.types.chat import ChatCompletionMessageParam

class OpenAiMessage(TypedDict):
   content: str
   role: Literal["system", "user", "assistant"]

# OpenAiCompletionModels = Literal[
#    "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4",
#    "gpt-3.5-turbo",
#    "o1-preview", "o1-mini"
# ]

OpenAiEmbeddingModels = Literal[
   "text-embedding-3-large", "text-embedding-3-small",
   "text-embedding-ada-002"
]

def load_openai_client(api_key: str | None = None):
   if api_key is None:
      logging.info("Loading dotenv to find OPENAI API key")
      load_dotenv()
      api_key = os.environ.get("OPENAI_API_KEY")
      if api_key is None:
         raise ValueError("api_key is None, and no loadable OPENAI_API_KEY")
   if not isinstance(api_key, str):
      raise ValueError("api_key is not a string")
   client = OpenAI(api_key=api_key)
   return client

def chat(
   messages: list[Message | ChatCompletionMessageParam | str] | str,
   model: ChatModel | str = "gpt-3.5-turbo", 
   api_key: str | None = None
):
   client = load_openai_client(api_key)
   chat_messages: list[ChatCompletionMessageParam] = []

   # I'm unsure if this dynamism is preferable - but I will test with personal experience.
   if isinstance(messages, list):
      for m in messages:
         if isinstance(m, Message):
            msg: Any = m.model_dump() # Could not solve this irritating type error without assigning to Any
            chat_messages.append(msg)
         elif isinstance(m, str):
            msg: Any = { "content": m, "role": "user" }
            chat_messages.append(msg)
         else:
            chat_messages.append(m)
   else:
      chat_messages.append({ "content": messages, "role": "user" })

   assert len(chat_messages) > 0, f"Messages filtered down unexpectedly: {messages}"

   chat_completion = client.chat.completions.create(
      messages=chat_messages,
      model=model,
   )

   return chat_completion

def chat_message(
   messages: list[Message | ChatCompletionMessageParam | str] | str,
   model: ChatModel | str = "gpt-3.5-turbo", 
   api_key: str | None = None,
   output: bool = False
):
   chat_completion = chat(messages, model, api_key)
   choices = chat_completion.choices
   if len(choices) > 1:
      logging.warning(f"More than 1 choice: choosing first option")
   choice = choices[0]
   # NOTE logprobs is removed here, I want to look into that in the future
   # NOTE https://cookbook.openai.com/examples/using_logprobs
   msg = choice.message
   if output:
      print(messages[-1])
      print(msg.content)
   return msg
   

def text_embedding(text: str, model: OpenAiEmbeddingModels): 
   ...