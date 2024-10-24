from flask import Flask, jsonify
#from gemini_api import generate
import functions.nutrition_functions as nf
import functions.exercise_functions as ef
from LLM_plan_generation.OpenAI.openai_api_mealplan_expensive import generate

app = Flask(__name__)

@app.route('/')
def home():
    ## Testing LLM Nutrition Function ##

    #data needed:
    '''
    Calories 
    Macros

    Preferences
    Number of Meals

    Diet Type:
    - Vegetarian
    - Vegan
    - Keto
    - Omnivore
    - Carnivore
    '''

    dummy_user_data_nutrition = {
    "weight": nf.lbs_to_kg(150),
    "height": nf.inches_to_cm(66),
    "age": 24,
    "is_male": True,
    "goal": "gain",
    "diet_type": "omnivore",
    "activity_level": "sedentary",
    "meal_number" : 3,
    "preferences" : "Chicken, chocolate milk",
    "avoid" : "liver"
    }
    dummy_nutriton_data = nf.get_nutrition_plan(dummy_user_data_nutrition)
    response = generate(dummy_nutriton_data)
    ## Testing LLM Nutrition Function ##
    '''
    ## Testing LLM Exercise Function ##
    dummy_user_data_exercise = {
    "weight": nf.lbs_to_kg(150),
    "height": nf.inches_to_cm(66),
    "age": 24,
    "is_male": True,
    "goal": "gain",
    "diet_type": "carnivore",
    "activity_level": "sedentary"
    }
    WorkoutPlanner = ef.WorkoutPlanner()
    dummy_exercise_data = WorkoutPlanner.plan_workout(60, 'Endurance')
    response = generate(dummy_nutriton_data)
    ## Testing LLM Exercise Function ##
    '''
    return response


if __name__ == '__main__':
    app.run(debug=True)



# from fastapi import FastAPI
# from gemini_api import generate

# app = FastAPI()

# @app.get('/')
# async def root():
#     return generate()
