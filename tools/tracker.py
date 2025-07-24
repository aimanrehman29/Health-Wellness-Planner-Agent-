from agents import function_tool, RunContextWrapper
from context import UserSessionContext

@function_tool
async def track_progress(
    progress: str, 
    ctx: RunContextWrapper[UserSessionContext]
) -> None:
    """
    Store progress updates in the session context and print the progress update.
    """
    if not hasattr(ctx.context, 'progress_logs'):
        ctx.context.progress_logs = [] 
    
    ctx.context.progress_logs.append({"progress": progress})

    print(f"Progress updated: {progress}")
