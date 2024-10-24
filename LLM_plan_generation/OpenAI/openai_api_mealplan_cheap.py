from openai import OpenAI
import time
client = OpenAI()

def generate(data=None):

    #data needed
    ##Calories 
    ##Macros
    ##Preferences
    ## Number of Meals
    ##Diet Type:
    '''
    - Vegetarian
    - Vegan
    - Keto
    - Omnivore
    - Carnivore
    '''

    calories = data['target_calories']

    ##  macros
    carbs = (data['macros']['carbs'])
    fat = (data['macros']['fat'])
    protein = (data['macros']['protein'])

    ##  diet type
    diet_type = data['diet_type']

    ## preferences
    preference_foods = data['preferences']
    ## avoid 
    avoid_foods = data['avoid']

    timeStart = time.time()

    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert nutritionist who builds nutrition plans tailored to your clients specific needs"},
            {
                "role": "user",
                "content":
                
                f"""
                    Step 1: Create a mealplan for a(n) {diet_type} client for {7} day(s) with {3} meals
                            They like {preference_foods} and will not eat {avoid_foods}
                    Calories: {calories}
                    Macros: 
                        Carbs: {carbs}
                        Fats: {fat}
                        Protein: {protein}


                    Step 2: Format the output to look like the following template, do not include nutritional information, include a list of ingredients for the mealplan at the end
                            There can be more than 2 foods each meal if needed, and meals/snacks can be cut to adhere to the requirements above
           
                    Template Mealplan:
                        ## Breakfast: <br>
                        - 4 of food <br>
                        - 5g of food <br>
                        - 4 of food <br>
                        ... etc
                        ## Lunch: <br>
                        - 8 oz food <br>
                        - 2 oz food <br>
                        ... etc
                        ## Snack: <br>
                        - 2 oz food <br>
                        ... etc 
                        ## Dinner: <br>
                        - 8 oz food <br>
                        - 2 oz food <br>
                        - 2 oz food <br>
                        ... etc 
                        ## Evening Snack:
                        - 3 food <br>
                        ... etc

                """
            }
        ]
    )


    mealplan = completion.choices[0].message.content

    timeEnd = time.time()
    

    #Output needs:
    #Meal
    ## Food 1
    ## Food 2... etc
    #Ingredients (done)
    #Directions (generated daily)

    return mealplan+"<br>Time to execute: "+str(timeEnd-timeStart)


