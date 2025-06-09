from abc import ABC, abstractmethod
from typing import List
from ..core.prompt import Prompt
from ..core.goals import Goal
from ..actions.action import Action
from ..memory.memory import Memory
from ..environment.environment import Environment

class AgentLanguage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def construct_prompt(self,
                         actions: List[Action],
                         environment: Environment,
                         goals: List[Goal],
                         memory: Memory) -> Prompt:
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def parse_response(self, response: str) -> dict:
        raise NotImplementedError("Subclasses must implement this method")