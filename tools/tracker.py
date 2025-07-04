from context import UserSessionContext
from agents import RunContextWrapper

class ProgressTrackerTool:
    def __init__(self):
        self.name = "Progress Tracker"

    async def track_progress(self, progress: str, ctx: RunContextWrapper[UserSessionContext]) -> None:
        # Store progress updates in the session context
        ctx.context.progress_logs.append({"progress": progress})
        print(f"Progress updated: {progress}")
