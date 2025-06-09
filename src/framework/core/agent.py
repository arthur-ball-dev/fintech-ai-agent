import json
from typing import List, Callable, Optional
from .prompt import Prompt
from .goals import Goal
from ..actions.registry import ActionRegistry
from ..language.base import AgentLanguage
from ..memory.memory import Memory
from ..environment.environment import Environment

class Agent:
    def __init__(self,
                 goals: List[Goal],
                 agent_language: AgentLanguage,
                 action_registry: ActionRegistry,
                 generate_response: Callable[[Prompt], str],
                 environment: Environment):
        self.goals = goals
        self.generate_response = generate_response
        self.agent_language = agent_language
        self.actions = action_registry
        self.environment = environment

    def construct_prompt(self, goals: List[Goal], memory: Memory, actions: ActionRegistry) -> Prompt:
        return self.agent_language.construct_prompt(
            actions=actions.get_actions(),
            environment=self.environment,
            goals=goals,
            memory=memory
        )

    def get_action(self, response):
        invocation = self.agent_language.parse_response(response)
        action = self.actions.get_action(invocation["tool"])
        return action, invocation

    def should_terminate(self, response: str) -> bool:
        action_def, _ = self.get_action(response)
        return action_def.terminal if action_def else False

    def set_current_task(self, memory: Memory, task: str):
        memory.add_memory({"type": "user", "content": task})

    def update_memory(self, memory: Memory, response: str, result: dict):
        new_memories = [
            {"type": "assistant", "content": response},
            {"type": "environment", "content": json.dumps(result)}
        ]
        for m in new_memories:
            memory.add_memory(m)

    def prompt_llm_for_action(self, full_prompt: Prompt) -> str:
        response = self.generate_response(full_prompt)
        return response

    def run(self, user_input: str, memory: Optional[Memory] = None, max_iterations: int = 50) -> Memory:
        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for _ in range(max_iterations):
            prompt = self.construct_prompt(self.goals, memory, self.actions)
            
            print("Agent thinking...")
            response = self.prompt_llm_for_action(prompt)
            print(f"Agent Decision: {response}")
            
            action, invocation = self.get_action(response)
            if not action:
                print(f"Unknown action: {invocation['tool']}")
                break
                
            result = self.environment.execute_action(action, invocation["args"])
            print(f"Action Result: {result}")
            
            self.update_memory(memory, response, result)
            
            if self.should_terminate(response):
                break

        return memory