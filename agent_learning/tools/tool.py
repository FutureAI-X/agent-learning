from typing import Any, Dict

from abc import ABC, abstractmethod

class Tool(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, parameters: Dict[str, Any]):
        pass

    @abstractmethod
    def get_parameters(self):
        pass