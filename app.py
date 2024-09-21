from flask import Flask, jsonify
from gemini_api import generate

app = Flask(__name__)

@app.route('/')
def home():
    response = generate()
    return response

if __name__ == '__main__':
    app.run(debug=True)



# from fastapi import FastAPI
# from gemini_api import generate

# app = FastAPI()

# @app.get('/')
# async def root():
#     return generate()
