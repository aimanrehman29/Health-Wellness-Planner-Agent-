from agents import function_tool, RunContextWrapper
from context import UserSessionContext

@function_tool
async def schedule_checkin(ctx: RunContextWrapper[UserSessionContext]) -> None:
    """
    Simulate scheduling a weekly check-in (e.g., reminder for progress updates).
    """
    print("Weekly progress check-in scheduled!")
    
    ctx.context.checkin_scheduled = True
