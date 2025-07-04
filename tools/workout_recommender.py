from typing import Dict
from context import UserSessionContext
from agents import RunContextWrapper

class WorkoutRecommenderTool:
    def __init__(self):
        self.name = "Workout Recommender"

    async def recommend_workout(self, goal: str, ctx: RunContextWrapper[UserSessionContext]) -> Dict:
        # A simple workout plan based on the goal
        workout_plan = {}

        if goal == "weight_loss":
            workout_plan = {
                "Day 1": "Cardio - 30 minutes of running",
                "Day 2": "Strength Training - Upper body",
                "Day 3": "Cardio - 30 minutes cycling",
                "Day 4": "Strength Training - Lower body",
                "Day 5": "Cardio - 30 minutes swimming",
                "Day 6": "Yoga or Stretching",
                "Day 7": "Rest"
            }
        else:
            workout_plan = {
                "Day 1": "Full-body workout",
                "Day 2": "Strength Training",
                "Day 3": "Cardio",
                "Day 4": "Rest",
                "Day 5": "Core workout",
                "Day 6": "Cardio",
                "Day 7": "Rest"
            }

        ctx.context.workout_plan = workout_plan
        return workout_plan
