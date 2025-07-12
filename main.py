import asyncio
import sys
import os
from context import UserSessionContext
from utils.stream_response import stream_response
from main_agent import PlannerAgent  
from dotenv import load_dotenv

# Importing the guardrails for input validation
from guardrails import validate_goal_input, validate_diet_preference, validate_injury_notes, validate_fitness_level, validate_non_empty_input

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = "https://openrouter.ai/api/v1"
model = "deepseek/deepseek-r1-0528:free"

async def main():
    # Create a UserSessionContext object
    ctx = UserSessionContext(name="Guest", uid=1)
    
    # Initialize the main agent (PlannerAgent)
    agent = PlannerAgent()

    instruction = """
    Please respond in English. You are a health and wellness agent. 
    You have to handoff to the appropriate agent based on the user's needs.
    Don't reply out of the health and wellness domain. 
    """

    print(">>> Health & Wellness Agent (type 'quit' to exit)")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break
        
        try:
            validate_non_empty_input(user_input)
            
            if "goal" in user_input.lower():
                validated_goal = validate_goal_input(user_input)
                print(f"Validated Goal: {validated_goal}")
            if "diet" in user_input.lower() or "meal" in user_input.lower():
                validated_diet = validate_diet_preference(user_input)
                print(f"Validated Diet: {validated_diet}")
            if "injury" in user_input.lower():
                validated_injury = validate_injury_notes(user_input)
                print(f"Validated Injury: {validated_injury}")
            if "fitness level" in user_input.lower():
                validated_level = validate_fitness_level(user_input)
                print(f"Validated Fitness Level: {validated_level}")
            
        except ValueError as e:
            print(f"Error: {e}")
            continue  
        
        user_input_with_instruction = f"{instruction} {user_input}"

        await stream_response(agent=agent, prompt=user_input_with_instruction, ctx=ctx)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())



