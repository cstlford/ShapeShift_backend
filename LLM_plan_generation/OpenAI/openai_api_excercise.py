from openai import OpenAI
client = OpenAI()

from LLM_search_tools.food_db import search_food_db
from LLM_search_tools.websearch_cheap import search


#ppl

def generate(data=None):


    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content":
                
                f"""
                Generate a workout that uses the following exercises:
                
                    Format the output to look like the following sample:
                      
                """
            }
        ]
    )

        
    mealplan = completion.choices[0].message.content


    return mealplan

'''
def generate_mealplan(data=None):

    for x in range(7):
        meaplplan = generate(data)
'''

