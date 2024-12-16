

import json
from pathlib import Path
from microai.models.chatgpt import chat_message
from microai.models.generic import Message, MessageRoles
from openai.types.chat_model import ChatModel


def line_strip(content: str) -> str:
   stripped_content = [l.strip() for l in content.split("\n")]
   return "\n".join(stripped_content)


class GPTChainAdders(object):
   history: list[Message]

   def add_content(self, content: str, role: MessageRoles, auto_line_strip: bool = True):
      if auto_line_strip:
         content = line_strip(content)
      self.history.append(Message(content=content, role=role))
      return self

   def add_user_content(self, content: str, auto_line_strip: bool = True):
      if auto_line_strip:
         content = line_strip(content)
      self.add_content(content, "user")
      return self
   
   def add_assistant_content(self, content: str, auto_line_strip: bool = True):
      if auto_line_strip:
         content = line_strip(content)
      self.add_content(content, "assistant")
      return self

   def add_system_content(self, content: str, auto_line_strip: bool = True):
      if auto_line_strip:
         content = line_strip(content)
      self.add_content(content, "system")
      return self

class GPTChain(GPTChainAdders):

   history: list[Message]
   model: ChatModel | None

   def __init__(self, model: ChatModel | None = None):
      self.history = []
      self.model = model

   def invoke_assistant_chain(self, model: ChatModel | None = None):
      if model is None:
         model = self.model
      if model is None:
         raise ValueError("No model specified")
      msg = chat_message(self.history, model)
      self.history.append(msg)
      return self

   def output_content(self):
      return self.history[-1].content
   
   def output_content_str(self):
      content = self.output_content()
      if content is None:
         raise ValueError("No output message content")
      return content

   def output_message(self):
      return self.history[-1]
   
   def output_parsed_list(self) -> list[str]:
      output_message = self.output_message()
      if output_message.content is None:
         raise ValueError("No output message content")
      content = output_message.content
      lines = content.split("\n")
      lines = [i.strip().strip('•-* ') for i in lines]
      lines = [i for i in lines if i]
      return lines

   def save_chain_history(self, path: Path):
      with open(path, "w") as f:
         f.write(json.dumps([h.model_dump() for h in self.history], indent=4))
      return self
   
   def slice_history(self, from_index: int, to_index: int | None = None):
      """This can be used to remove sections of the history as needed. This can reduce
      the size of the context window for the model, and it can also remove backreference information
      which can be confusing for the model as it works through its chain."""
      if to_index is None:
         to_index = len(self.history)
      self.history = self.history[from_index:to_index]
      return self
