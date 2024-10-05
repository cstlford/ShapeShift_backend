from openai import OpenAI
client = OpenAI()

from food_db import search_food_db
from websearch_cheap import search



def generate(data=None):

    calories = data['target_calories']

    ##  macros
    carbs = data['macros']['carbs']
    fat = data['macros']['fat']
    protein = data['macros']['protein']

    ##  diet type
    diet_type = data['diet_type']
    

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content":
                
                f"""
                Generate a sample {diet_type} mealplan for 7 day for a user that needs to eat {calories} calories of food in a day. 
                    They should also hit the following macros:
                        Daily Carbs: {carbs}
                        Daily Fat: {fat}
                        Daily Protein: {protein}
                    Format the output to look like the following sample (there can be more than 2 foods each meal if needed):
                        # Day 1 <br>
                        ## Breakfast: <br>
                        - 4 of food [x calories, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 4 of food [x calories, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 4 of food [x calories, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc
                        ## Lunch: <br>
                        - 8 oz food [x calories, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 2 oz food [x calories, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc
                        ## Snack: <br>
                        - 2 oz food [x calories, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc 
                        ## Dinner: <br>
                        - 8 oz food [x calories, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 2 oz food [x calories, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 2 oz food [x calories, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc 
                        ## Evening Snack:
                        - 3 food [x calories, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc
                        ### Totals: - Calories: x - Fat: [x]g - Carbs: [x]g - Protein: [x]g <br>
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

