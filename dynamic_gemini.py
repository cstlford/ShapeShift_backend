"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai
from gemini_with_grounding_starter import generate_vertex_repsonse

chat_history = []

def generate(search_string = ""):
    genai.configure(api_key=os.environ["google_api_key"])

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=[
            
            """
               You are a helpful assistant
            """
        
        
        ],
    )
  
    # Start the chat session
    chat_session = model.start_chat(history=chat_history)

    # Send message to the model
    response = chat_session.send_message(search_string)

    chat_history.extend(chat_session.history)

    # Check for the specific phrase about lacking real-time info and provide a grounded response
    if "I do not have access to real-time information" in response.text:
        print("Grounded response enabled")
        grounded_response = chat_session.send_message(generate_vertex_repsonse(search_string))
        return grounded_response.text
    else:
        print("Normal response enabled")
        return response.text

