import re
from typing import List, Dict
from context import UserSessionContext
from agents import RunContextWrapper, Agent
from custom_agents.nutrition_expert_agent import NutritionExpertAgent
from custom_agents.injury_support_agent import InjurySupportAgent
from custom_agents.escalation_agent import EscalationAgent
from tools.goal_analyzer import GoalAnalyzerTool
from tools.meal_planner import MealPlannerTool
from tools.workout_recommender import WorkoutRecommenderTool
from tools.scheduler import CheckinSchedulerTool
from tools.tracker import ProgressTrackerTool
from fpdf import FPDF
from hooks import on_agent_start, on_agent_end, on_tool_start, on_tool_end, on_handoff

class PlannerAgent(Agent):
    def __init__(self):
        super().__init__(name="Health & Wellness Planner")
        self.output_type = "str"
        self.awaiting_workout_details = False

    async def stream(self, user_input: str, context_wrapper: RunContextWrapper[UserSessionContext]):
        on_agent_start(self, context_wrapper)

        try:
            ctx = context_wrapper.context
            user_input_lower = user_input.lower()

            # Handle user answers to workout questions
            if self.awaiting_workout_details:
                self._collect_workout_info(user_input_lower, ctx)
                if self._has_enough_workout_info(ctx):
                    on_tool_start(self, "WorkoutRecommenderTool", context_wrapper)
                    workout_tool = WorkoutRecommenderTool()
                    plan = await workout_tool.recommend_workout(ctx.fitness_goal, context_wrapper)
                    on_tool_end(self, "WorkoutRecommenderTool", context_wrapper)

                    response = "Here is your personalized workout plan:\n" + "\n".join(
                        f"{day}: {activity}" for day, activity in plan.items()
                    )
                    self.awaiting_workout_details = False
                else:
                    response = "Thanks! Please provide more details (goal, fitness level, days, equipment, etc.)."
                await self.send_response(response)
                on_agent_end(self, context_wrapper)
                return

            # Handoff Triggers
            if "diet" in user_input_lower or "meal" in user_input_lower:
                await self.handoff_to_nutrition_expert(context_wrapper)
                await self.send_response("You’ve been connected to our Nutrition Expert.")
            elif "injury" in user_input_lower:
                await self.handoff_to_injury_support(context_wrapper)
                await self.send_response("You're now speaking with the Injury Support Assistant.")
            elif "human" in user_input_lower or "talk to a person" in user_input_lower:
                await self.handoff_to_escalation_agent(context_wrapper)
                await self.send_response("Connecting you to a human assistant.")
            elif "workout" in user_input_lower or "exercise" in user_input_lower:
                self.awaiting_workout_details = True
                await self.send_response(
                    "Certainly! I can help you with that. To give you the best workout plan, I need a little more information. Please tell me:\n\n"
                    "*   **What are your fitness goals?** (e.g., build muscle, lose weight)\n"
                    "*   **What is your current fitness level?** (e.g., beginner, intermediate)\n"
                    "*   **How many days a week do you want to work out?**\n"
                    "*   **Do you have access to a gym or work out at home?**\n"
                    "*   **Any equipment available?** (e.g., dumbbells, bands)\n"
                    "*   **Any injuries or limitations I should know about?**"
                )
            elif "show my plan" in user_input_lower:
                # Show summary of the plan
                workout_plan = ctx.workout_plan
                meal_plan = ctx.meal_plan
                goal = ctx.fitness_goal
                summary = f"Your wellness plan:\nGoal: {goal}\nMeal Plan: {'\n'.join(meal_plan)}\nWorkout Plan: {'\n'.join(workout_plan)}"
                await self.send_response(summary)
            elif "export my plan" in user_input_lower:
                # Export to PDF
                plan_data = [
                    f"Goal: {ctx.fitness_goal}",
                    f"Meal Plan: {'\n'.join(ctx.meal_plan)}",
                    f"Workout Plan: {'\n'.join(ctx.workout_plan)}"
                ]
                self.generate_pdf(plan_data)  # This will create a PDF
                response = "Your wellness plan has been exported to PDF!"
                await self.send_response(response)
            else:
                await self.send_response("I can help create a wellness plan for you. Tell me about your goals or say 'I need a workout plan'.")

            on_agent_end(self, context_wrapper)

        except Exception as e:
            await self.send_response(f"❌ Error: {str(e)}")

    def _collect_workout_info(self, user_input: str, ctx: UserSessionContext):
        # Basic NLP: grab workout-related info based on keywords
        if "build muscle" in user_input:
            ctx.fitness_goal = "muscle_gain"
        elif "lose weight" in user_input:
            ctx.fitness_goal = "weight_loss"
        elif "general" in user_input:
            ctx.fitness_goal = "general_fitness"

        if "beginner" in user_input:
            ctx.fitness_level = "beginner"
        elif "intermediate" in user_input:
            ctx.fitness_level = "intermediate"
        elif "advanced" in user_input:
            ctx.fitness_level = "advanced"

        if "3" in user_input or "three" in user_input:
            ctx.workout_days = 3
        elif "5" in user_input or "five" in user_input:
            ctx.workout_days = 5
        elif "7" in user_input or "every day" in user_input:
            ctx.workout_days = 7

        if "gym" in user_input:
            ctx.equipment = "gym"
        elif "home" in user_input:
            ctx.equipment = "home"
        elif "dumbbells" in user_input or "bands" in user_input:
            ctx.equipment = "dumbbells/bands"

        if "back pain" in user_input or "injury" in user_input:
            ctx.injury_notes = "back pain"

    def _has_enough_workout_info(self, ctx: UserSessionContext) -> bool:
        return bool(ctx.fitness_goal and ctx.fitness_level and ctx.workout_days)

    def generate_pdf(self, plan_data, filename="wellness_plan.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in plan_data:
            pdf.cell(200, 10, txt=line, ln=True, align="L")
        pdf.output(filename)

    async def handoff_to_nutrition_expert(self, context_wrapper: RunContextWrapper[UserSessionContext]):
        on_handoff(self, "NutritionExpertAgent", context_wrapper)
        agent = NutritionExpertAgent(name="NutritionExpert")
        async for _ in agent.stream("nutrition help", context_wrapper):
            break

    async def handoff_to_injury_support(self, context_wrapper: RunContextWrapper[UserSessionContext]):
        on_handoff(self, "InjurySupportAgent", context_wrapper)
        agent = InjurySupportAgent(name="InjurySupport")
        async for _ in agent.stream("injury help", context_wrapper):
            break

    async def handoff_to_escalation_agent(self, context_wrapper: RunContextWrapper[UserSessionContext]):
        on_handoff(self, "EscalationAgent", context_wrapper)
        agent = EscalationAgent(name="Escalation")
        async for _ in agent.stream("escalate to human", context_wrapper):
            break

# Initialize the agent with tools and handoffs
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
