from flask import Flask, jsonify
from gemini_api import generate

app = Flask(__name__)

@app.route('/')
def home():
    response = generate()
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

"""
This is an Api. This is pretty much exactly what my Api looks like in fast Api 
from fastapi import FastAPI
from gemini import generate

app = FastAPI()

@app.get('/')
async def root():
    return generate()
This is what the fast Api api looks like. Its async though so maybe that is the difference.

"""