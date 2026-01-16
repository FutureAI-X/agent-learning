from typing import Optional
from abc import ABC, abstractmethod

from agent_learning.llms.openai_compatible_client import OpenAICompatibleClient
from agent_learning.messages.message import Message

class Agent(ABC):
    def __init__(
        self,
        name: str,
        llm_client: OpenAICompatibleClient,
        system_prompt: Optional[str] = None
    ):
        self.name = name,
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self._history: list[Message] = []

    @abstractmethod
    def run(self, input_text: str, **kwargs):
        """子类实现此方法"""
        pass

    def add_message(self, message: Message):
        self._history.append(message)

    def clear_history(self):
        self._history.clear()

    def get_history(self):
        return self._history.copy()

    def __str__(self):
        return f"Agent(name={self.name}, provider={self.llm_client.provider})"