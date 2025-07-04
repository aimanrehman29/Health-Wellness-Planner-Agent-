import re
from typing import List, Dict
from context import UserSessionContext
from agents import RunContextWrapper
from custom_agents.nutrition_expert_agent import NutritionExpertAgent
from custom_agents.injury_support_agent import InjurySupportAgent
from custom_agents.escalation_agent import EscalationAgent
from tools.goal_analyzer import GoalAnalyzerTool
from tools.meal_planner import MealPlannerTool
from tools.workout_recommender import WorkoutRecommenderTool
from tools.scheduler import CheckinSchedulerTool
from tools.tracker import ProgressTrackerTool
from agents import Agent

from hooks import on_agent_start, on_agent_end, on_tool_start, on_tool_end, on_handoff
from tools.goal_analyzer import GoalAnalyzerTool
from tools.meal_planner import MealPlannerTool
from tools.workout_recommender import WorkoutRecommenderTool

class PlannerAgent(Agent):
    def __init__(self):
        super().__init__(name="Health & Wellness Planner")
        self.output_type = "str"

    async def stream(self, user_input: str, context_wrapper: RunContextWrapper[UserSessionContext]):
        on_agent_start(self, context_wrapper)

        try:
            on_tool_start(self, "GoalAnalyzerTool", context_wrapper)
            goal_analyzer = GoalAnalyzerTool()
            goal_response = await goal_analyzer.analyze_goal(context_wrapper, user_input)
            on_tool_end(self, "GoalAnalyzerTool", context_wrapper)


            response = "I can help create a plan for you."

            if "nutrition" in user_input.lower():
                await self.handoff_to_nutrition_expert(context_wrapper)
            elif "injury" in user_input.lower():
                await self.handoff_to_injury_support(context_wrapper)
            elif "escalate" in user_input.lower():
                await self.handoff_to_escalation_agent(context_wrapper)

            await self.send_response(response)

            on_agent_end(self, context_wrapper)

        except Exception as e:
            print(f"Error: {str(e)}")

    async def handoff_to_nutrition_expert(self, context_wrapper: RunContextWrapper[UserSessionContext]):
        on_handoff(self, "NutritionExpertAgent", context_wrapper)
        nutrition_agent = NutritionExpertAgent(name="NutritionExpert")
        async for response in nutrition_agent.stream("nutrition help", context_wrapper):
            return response
    
    async def handoff_to_injury_support(self, context_wrapper: RunContextWrapper[UserSessionContext]):
        on_handoff(self, "InjurySupportAgent", context_wrapper)
        injury_agent = InjurySupportAgent(name="InjurySupport")
        async for response in injury_agent.stream("injury help", context_wrapper):
            return response
    
    async def handoff_to_escalation_agent(self, context_wrapper: RunContextWrapper[UserSessionContext]):
        on_handoff(self, "EscalationAgent", context_wrapper)
        escalation_agent = EscalationAgent(name="Escalation")
        async for response in escalation_agent.stream("escalate to human", context_wrapper):
            return response

agent = Agent(
    name="WellnessPlannerAgent",
    tools=[
        GoalAnalyzerTool(),
        MealPlannerTool(),
        WorkoutRecommenderTool(),
        CheckinSchedulerTool(),
        ProgressTrackerTool()
    ],
    handoffs={
        "nutrition": NutritionExpertAgent(name="NutritionExpert"),
        "injury": InjurySupportAgent(name="InjurySupport"),
        "human": EscalationAgent(name="Escalation")
    }
)



