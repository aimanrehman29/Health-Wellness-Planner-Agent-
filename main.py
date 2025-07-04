import asyncio
import sys
import os
from context import UserSessionContext
from utils.stream_response import stream_response 
from main_agent import PlannerAgent  
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = "https://openrouter.ai/api/v1"
model = "deepseek/deepseek-r1-0528:free"

async def main():
    ctx = UserSessionContext(name="Guest", uid=1)
    
    agent = PlannerAgent()

    instruction = """
    Please respond in English. You are a health and wellness agent. 
    You have to handoff to the appropriate agent based on the user's needs.
    Don't reply out of the health and wellness domain. 
    
    1. If the user asks for nutrition, handoff to the NutritionExpertAgent.
    2. If the user asks for injury support, handoff to the InjurySupportAgent.
    3. If the user asks for human support, handoff to the EscalationAgent.
    4. If the user asks for workout recommendations, use the WorkoutRecommenderTool.
    """

    print(">>> Health & Wellness Agent (type 'quit' to exit)")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break
        
        user_input_with_instruction = f"{instruction} {user_input}"

        await stream_response(agent=agent, prompt=user_input_with_instruction, ctx=ctx)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

