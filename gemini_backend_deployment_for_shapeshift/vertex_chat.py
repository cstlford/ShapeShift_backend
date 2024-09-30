import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
import os

# If grounding import is giving issues try pip install --upgrade google-cloud-aiplatform

def generate_vertex_repsonse(user_input):
    
    from vertexai.generative_models import (
        GenerationConfig,
        GenerativeModel,
        Tool,
        grounding,
    )

    project = os.getenv("vertex_project_name")

    vertexai.init(project=project, location="us-central1")

    model = GenerativeModel(
        "gemini-1.5-flash-002",

        system_instruction=[

            """
                "You are a nutrition expert who provides professional support for clients.",
                "You counsel people about nutrition using real-time data",
                "You provide emotional support for weight loss and weight gain",
                "You have a fun and engaging personality",
                "Make responses as concise as possible without leaving out any details",
            """


        ],

        )
    chat_session = ChatSession(model=model)
    
   


    # Use Google Search for grounding
    tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())


    response =  chat_session.send_message(
        user_input,
        tools=[tool],
        generation_config=GenerationConfig(
            temperature=0.0,
        ),
    )
    return response.text.strip().split("\n")
