import re

# 1. Goal Input Validation
def validate_goal_input(goal: str):
    """
    Validate fitness goal input in the format of "quantity metric in duration"
    E.g., "lose 5kg in 2 months"
    """
    goal_pattern = r"^([a-zA-Z\s]+)\s(\d+)([a-zA-Z]+)\s(in)\s(\d+)\s(months?|weeks?)$"
    match = re.match(goal_pattern, goal)
    if not match:
        raise ValueError("Invalid goal format. Please follow the format: 'lose 5kg in 2 months'")
    return match.groups()

# 2. Diet Preference Validation
valid_diets = ["vegetarian", "vegan", "gluten-free", "diabetic-friendly"]
def validate_diet_preference(diet_preference: str):
    """
    Validate dietary preferences (vegetarian, vegan, gluten-free, diabetic-friendly).
    """
    if diet_preference.lower() not in valid_diets:
        raise ValueError(f"Invalid diet. Choose from: {', '.join(valid_diets)}.")
    return diet_preference

# 3. Injury Notes Validation
valid_injuries = ["back pain", "knee pain", "shoulder injury", "ankle sprain"]
def validate_injury_notes(injury_notes: str):
    """
    Validate injury input. Ensure it's one of the valid injuries.
    """
    if injury_notes.lower() not in valid_injuries:
        raise ValueError(f"Invalid injury. Choose from: {', '.join(valid_injuries)}.")
    return injury_notes

# 4. Fitness Level Validation
valid_levels = ["beginner", "intermediate", "advanced"]
def validate_fitness_level(fitness_level: str):
    """
    Validate fitness level input (beginner, intermediate, advanced).
    """
    if fitness_level.lower() not in valid_levels:
        raise ValueError(f"Invalid fitness level. Choose from: {', '.join(valid_levels)}.")
    return fitness_level

# 5. General User Input Validation
def validate_non_empty_input(user_input: str):
    """
    Ensure that user input is not empty.
    """
    if not user_input or user_input.strip() == "":
        raise ValueError("Input cannot be empty.")
    return user_input
