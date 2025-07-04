# custom_agents/escalation_agent.py

from context import UserSessionContext
from agents import RunContextWrapper, Agent

class EscalationAgent(Agent):
    def __init__(self, name: str):
        self.name = name

    async def stream(self, user_input: str, context_wrapper: RunContextWrapper[UserSessionContext]):
        """
        Handle human escalation requests.
        """
        response = f"Escalating to a human for: {user_input}"
        yield {"text": response}
