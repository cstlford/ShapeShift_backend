import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
import os
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    Tool,
    grounding,
)

#project = os.getenv("vertex_project_name")

vertexai.init(project="golden-context-430621-t6", location="us-central1")

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
print("Welcome to gemini search. Type quit! to exit")
while(True):
    user_input = input("Enter text here:").lower().strip()
    if(user_input == "quit!"):
        break
    
    response =  chat_session.send_message(
        user_input,
        tools=[tool],
        generation_config=GenerationConfig(
            temperature=0.0,
        ),
    )
    
    
    print(response.text)