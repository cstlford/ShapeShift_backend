from flask import Flask, jsonify
#from gemini_api import generate
import nutrition_functions as nf
from openai_api import generate

app = Flask(__name__)

@app.route('/')
def home():
    ## Testing LLM Function ##
    dummy_data = {
    "weight": nf.lbs_to_kg(150),
    "height": nf.inches_to_cm(66),
    "age": 24,
    "is_male": True,
    "goal": "gain",
    "diet_type": "carnivore",
    "activity_level": "sedentary"
    }
    data = nf.get_nutrition_plan(dummy_data)
    response = generate(data)
    ## Testing LLM Function ##
    
    return response


if __name__ == '__main__':
    app.run(debug=True)



# from fastapi import FastAPI
# from gemini_api import generate

# app = FastAPI()

# @app.get('/')
# async def root():
#     return generate()
