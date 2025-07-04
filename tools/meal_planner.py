from typing import List
from context import UserSessionContext
from agents import RunContextWrapper

class MealPlannerTool:
    def __init__(self):
        self.name = "Meal Planner"

    async def generate_meal_plan(self, ctx: RunContextWrapper[UserSessionContext]) -> List[str]:
        meal_plan = [
            "Day 1: Grilled tofu with quinoa",
            "Day 2: Vegetable stir-fry with rice",
            "Day 3: Lentil soup with bread",
            "Day 4: Veggie burger with a salad",
            "Day 5: Chickpea curry with rice",
            "Day 6: Vegan burrito with avocado",
            "Day 7: Pasta with tomato basil sauce"
        ]
        ctx.context.meal_plan = meal_plan
        return meal_plan
