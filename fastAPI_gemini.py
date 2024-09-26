from fastapi import FastAPI
from gemini_with_grounding_starter import generate_vertex_repsonse
from fastapi.middleware.cors import CORSMiddleware
from dynamic_gemini import generate

# To start with live reload use command uvicorn fastAPI_gemini:app --reload

app = FastAPI()
conversation_history = ""
origins = [
    "http://localhost:3000",  # Add this origin
    "http://localhost:5173",  # Ensure this has the full URL
    "http://localhost:5174", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/generate/{query}")

async def root(query):
    
    return generate(query)

   
