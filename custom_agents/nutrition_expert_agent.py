# custom_agents/nutrition_expert_agent.py
from context import UserSessionContext
from agents import RunContextWrapper, Agent


class NutritionExpertAgent(Agent):
    def __init__(self, name: str):
        self.name = name

    async def stream(self, user_input: str, context_wrapper: RunContextWrapper[UserSessionContext]):
        """
        Handle nutrition-related requests.
        """
        response = f"Providing nutrition advice for: {user_input}"
        yield {"text": response}


