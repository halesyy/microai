
from typing import Any
from microai.models.chatgpt import chat_message
from microai.models.generic import Message


def main():
   history: list[Any] = ["Hi mate how are you, guess where I am from based on how I said hi"]
   history.append(chat_message(history))
   message = chat_message(history + ["Yes!"])

if __name__ == "__main__":
   main()