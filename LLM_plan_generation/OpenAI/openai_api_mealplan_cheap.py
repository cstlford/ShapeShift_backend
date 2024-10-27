from openai import OpenAI
import time
import re
client = OpenAI()

def generate(data=None):

    '''
    User data -> LLM generated mealplan (Cheap, takes less time/money)
    '''

    #User data

    ## calories
    calories = data['target_calories']

    ## macros
    carbs = (data['macros']['carbs'])
    fat = (data['macros']['fat'])
    protein = (data['macros']['protein'])

    ## diet type
    diet_type = data['diet_type']
    '''
    - Vegetarian
    - Vegan
    - Keto
    - Omnivore
    - Carnivore
    '''

    ## preferences
    preference_foods = data['preferences']
    meal_number = data['meal_number']
    plan_number = 7
    ## avoid 
    avoid_foods = data['avoid']


    #LLM generation 

    ##!! FIXME: INCLUDE INGREDIENT LIST FOR GROCERY SHOPPERS !!##
    ## Prompt 1 -> Generate meal plan
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert nutritionist who builds nutrition plans tailored to your clients specific needs"},
            {
                "role": "user",
                "content":
                
                f"""
                    Step 1: Create a mealplan for a(n) {diet_type} client for {plan_number} day(s) with {meal_number} meals
                            They like {preference_foods} and will not eat {avoid_foods}
                    Calories: {calories}
                    Macros: 
                        Carbs: {carbs}
                        Fats: {fat}
                        Protein: {protein}


                    Step 2: Format the output to look like the following template, do not include nutritional information
                            There can be more than 2 foods each meal if needed
                            Feel free to add/subtract the amount of meals below, as long as there are {meal_number} main meals
                    Template Mealplan:
                        ## Day 1 <br>
                        ### *Breakfast: <br>
                        - 4 of food <br>
                        - 5g of food <br>
                        - 4 of food <br>
                        ... etc
                        #### Preparation Steps: <br>
                        - Step 1 <br>
                        - Step 2 <br>
                        - Step 3 <br>
                        ... etc
                        ### *Lunch: <br>
                        - 8 oz food <br>
                        - 2 oz food <br>
                        ... etc
                        #### Preparation Steps: <br>
                        - Step 1 <br>
                        - Step 2 <br>
                        - Step 3 <br>
                        ... etc
                        ### *Snack: <br>
                        - 2 oz food <br>
                        ... etc
                        #### Preparation Steps: <br>
                        - Step 1 <br>
                        - Step 2 <br>
                        - Step 3 <br>
                        ..etc
                        ### *Dinner: <br>
                        - 8 oz food <br>
                        - 2 oz food <br>
                        - 2 oz food <br>
                        ... etc
                        #### Preparation Steps: <br>
                        - Step 1 <br>
                        - Step 2 <br>
                        - Step 3 <br>
                        ..etc
                        ### *Evening Snack: <br>
                        - 3 food <br>
                        ... etc
                        #### Preparation Steps: <br>
                        - Step 1 <br>
                        - Step 2 <br>
                        - Step 3 <br>
                        ..etc
                """
            }
        ]
    )

    mealplan = completion.choices[0].message.content

    # format data
    meals = []
    plan = []

    startpoint = 0

    for day in range(plan_number):
        text = mealplan[startpoint:]

        ## find meals for day
        if day != plan_number-1:
            span = re.search(f"## Day {day+2} <br>\n", text)
            meals = re.findall(r"### \*.*:", text[:span.end()])
        else:
            meals = re.findall(r"### \*.*:", text)

        print(meals)
        
        ## find foods for each meal
        dayObject = []
        for meal in meals:
            text = mealplan[startpoint:]

            ### clean meals
            index = meal.find(':')
            meal = meal[5:index]
            
            ### get meal group 
            span = re.search(r"### \*.*: <br>\n(-.* <br>\n)*", text)
            
            ### get ingredients
            ingredients = re.findall(r"-.* <br>\n", text[span.start():span.end()])

            ### get/clean ingredients
            for index in range(len(ingredients)):
                ingredients[index] = re.search(r"-(.*)<br>\n", ingredients[index]).group(1)
                    
            ### get directions group
            span = re.search(r"####.*: <br>\n(- Step.*<br>\n)*", text)

            ### get directions
            directions = re.findall(r"-.* <br>\n", text[span.start():span.end()])

            ### clean directions
            for index in range(len(directions)):
                directions[index] = re.search(r"- (Step.*)<br>\n*", directions[index]).group(1)

            ### prepare for next cycle
            startpoint += span.end() 
            
            ### set object
            mealObject = {"title" : meal,
                            "calories": None,
                            "macros": None,
                            "ingredients": ingredients,
                            "directions" : directions
                        }

            dayObject.append(mealObject)
        plan.append(dayObject)
    print(plan)
    return(mealplan)



