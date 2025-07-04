# custom_agents/injury_support_agent.py
from context import UserSessionContext
from agents import RunContextWrapper, Agent

class InjurySupportAgent(Agent):
    def __init__(self, name: str):
        self.name = name

    async def stream(self, user_input: str, context_wrapper: RunContextWrapper[UserSessionContext]):
        """
        Handle injury-related requests.
        """
        response = f"Providing injury help for: {user_input}"
        yield {"text": response}

