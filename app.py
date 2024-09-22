from flask import Flask, jsonify
from gemini_api import generate

app = Flask(__name__)

@app.route('/')
def home():
    ## Testing LLM Function ##
    data = {
        'target_calories': 2500, 'macros': {'protein': 128, 'fat': 78, 'carbs': 323}
    }
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
