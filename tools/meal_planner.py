from typing import List
from agents import function_tool, RunContextWrapper
from context import UserSessionContext

@function_tool
async def generate_meal_plan(
    ctx: RunContextWrapper[UserSessionContext]
) -> List[str]:
    """
    Generate a weekly meal plan and store it in the user session context.
    """
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
