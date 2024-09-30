"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai
def generate_meal_plan():
        genai.configure(api_key=os.environ["google_api_key"])

        # Create the model
        generation_config = {
          "temperature": 1,
          "top_p": 0.95,
          "top_k": 40,
          "max_output_tokens": 8192,
          "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
          system_instruction="""
                You role is to create meal plans for the user.
                Send markdown that will be used on the front end.
            

          """,
          model_name="gemini-1.5-flash-002",
          generation_config=generation_config,
          # safety_settings = Adjust safety settings
          # See https://ai.google.dev/gemini-api/docs/safety-settings
        )

        chat_session = model.start_chat(
          history=[
          ]
        )

        response = chat_session.send_message(f"Send markdown for a 3 day meal plan")

        return response.text
