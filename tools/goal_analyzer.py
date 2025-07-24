from typing import Dict
from pydantic import BaseModel
from context import UserSessionContext
from agents import function_tool, RunContextWrapper

class GoalInput(BaseModel):
    quantity: float
    metric: str
    duration: str

# Functional tool version of analyze_goal
@function_tool
async def analyze_goal(
    ctx: RunContextWrapper[UserSessionContext], 
    input: GoalInput
) -> Dict:
    """
    Parse and validate a user's fitness goal (e.g., 'lose 5 kg in 3 months'),
    save it in the user session context, and return as JSON.
    """
    goal_dict = input.dict()

    ctx.context.goal = goal_dict

    return {"parsed_goal": goal_dict}
