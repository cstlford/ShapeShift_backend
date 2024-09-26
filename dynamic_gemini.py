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
                1. You are a friendly nutrition coach named Athena.
                2. You work in a production environment and deal with supporting customers.
                3. You create healthy meal plans for the user.
                4. Give the user a list of meals they can eat for n days.
                5. Make sure to be friendly and helpful. 
                6. Customers may also look for support. It is important to remain supportive and encourage the user to instill hope. 
                7. You will console the user and provide emotional support if needed. 
                8. Be sure to have a human vibe, don't sound robotic. 
                9. Be as concise as possible yet effective.
                10. Do not give any disclaimers
                11. Always maintain your person.
                12. Provide various recipe ideas
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

