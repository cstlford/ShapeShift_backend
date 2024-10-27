from openai import OpenAI
import time
import re



def calculate(nutrient,output):

    '''
    LLM Output + Given Nutritional info -> % Error 
    '''

    sum = 0

    # search for all instances of nutrient 
    if nutrient == "calories":
        regex = "(\d{1,4})( cals)"
    else:
        regex = "(\d{1,4})(g "+nutrient+")"
    amounts = re.findall(regex, output)

    # sum nutrient
    for amount in amounts:
        sum += int(amount[0])
    return sum

## FIXME: Suggest tweaks to mealplan based on calories and corresponding macros
def check(output, calories, fat, carbs, protein):

    '''
    LLM Output + Given Nutritional info -> % Error 
    '''

    # extract macro information from given values
    fat = int(re.search(r"\d{1,4}", fat).group())
    carbs = int(re.search(r"\d{1,4}", carbs).group())
    protein = int(re.search(r"\d{1,4}", protein).group())

    # extract calorie/macro sums from generated response
    gen_calories = calculate("calories",output)
    gen_fat = calculate("fat",output)
    gen_carbs = calculate("carbs",output)
    gen_protein = calculate("protein",output)
    
    # supply % error
    print(
        f'''
        Start {calories} => Generated {gen_calories} Error: {abs(calories - gen_calories)/calories}
        Start {fat} => Generated {gen_fat} Error: {abs(fat - gen_fat)/fat}
        Start {carbs} => Generated {gen_carbs} Error: {abs(carbs - gen_carbs)/carbs}
        Start {protein} => Generated {gen_protein} Error: {abs(protein - gen_protein)/protein}
        '''
    )


def generate(data=None):

    '''
    User data -> LLM generated mealplan (Expensive, takes more time/money)
    '''

    #Get user data

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
    ## avoid 
    avoid_foods = data['avoid']


    #LLM generation 

    client = OpenAI()

    ## Prompt 1 -> generate foodlist 
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert nutritionist who builds nutrition plans tailored to your clients specific needs"},
            {
                "role": "user",
                "content":
                
                f"""
                    Step 1: Find a list of about 20 healthy, diverse foods to be used in a mealplan for a(n) {diet_type} client.
                            The client likes {preference_foods} and will not eat {avoid_foods}

                    Step 2: Gather nutritional information for each food found in the 1st step corresponding to its serving size

                    Return the list
                """
            }
        ]
    )

    foodlist = completion.choices[0].message.content
    
    ## Prompt 2 -> build nutrition plan
    completion1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert nutritionist who builds nutrition plans tailored to your clients specific needs"},
            {
                "role": "user",
                "content":
                
                f"""
                    Step 1: Create a mealplan for a(n) {diet_type} client for {1} day(s) with {meal_number} meals using the following foods and their nutritional information:

                    Foods: 
                        {foodlist}


                    Step 2: After the mealplan has been created, audit the mealplan to fit the following nutritional requirements:
                        Daily Calories: {calories}
                        Daily Carbs: {carbs}
                        Daily Fat: {fat}
                        Daily Protein: {protein}


                    Step 3: Format the output to look like the following sample (there can be more than 2 foods each meal if needed)           
                            Feel free to add/subtract the amount of meals below, as long as there are {meal_number} main meals
                            Only include '*" in front of meal names
                    Sample Mealplan:
                        ## Day {1} <br>
                        ### *Breakfast: <br>
                        - 4 of food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 4 of food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 4 of food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc
                        #### Preparation Steps: <br>
                        - Step 1 <br>
                        - Step 2 <br>
                        - Step 3 <br>
                        ... etc
                        ### *Lunch: <br>
                        - 8 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 2 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc
                        #### Preparation Steps: <br>
                        - Step 1 <br>
                        - Step 2 <br>
                        - Step 3 <br>
                        ... etc
                        ### *Snack: <br>
                        - 2 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc
                        #### Preparation Steps: <br>
                        - Step 1 <br>
                        - Step 2 <br>
                        - Step 3 <br>
                        ... etc
                        ### *Dinner: <br>
                        - 8 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 2 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 2 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc
                        #### Preparation Steps: <br>
                        - Step 1 <br>
                        - Step 2 <br>
                        - Step 3 <br>
                        ... etc
                        ### *Evening Snack:
                        - 3 food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc
                        #### Preparation Steps: <br>
                        - Step 1 <br>
                        - Step 2 <br>
                        - Step 3 <br>
                        ... etc
                        ### Totals: - Calories: x - Fat: [x]g - Carbs: [x]g - Protein: [x]g <br>
                """
            }
        ]
    )

    mealplan = completion1.choices[0].message.content

    ## Check output for accuracy
    check(mealplan, calories, fat, carbs, protein)


    # format data
    meals = []
    plan = []

    startpoint = 0

    meals = re.findall(r"### \*.*:", mealplan)
        
    ## find foods for each meal
    for meal in meals:
        meal_cals = 0
        meal_fat = 0
        meal_carbs = 0
        meal_protein = 0

        text = mealplan[startpoint:]

        ### clean meals
        index = meal.find(':')
        meal = meal[5:index]
        
        ### get meal group 
        span = re.search(r"### \*.*: <br>\n(-.* <br>\n)*", text)
        
        ### get ingredients
        ingredients = re.findall(r"-.* <br>\n", text[span.start():span.end()])

        ### clean ingredients
        for index in range(len(ingredients)):
            # get ingredient properties (name, # cals, # fat, # carbs, # protein)
            ingredient = re.search(r"-(.*) \[(.*) cals, (.*)g fat, (.*)g carbs, (.*)g protein\]", ingredients[index])

            # add name/amount of ingredient to ingredients list
            ingredients[index] = ingredient.group(1)

            # add nutritional info to meal variables
            meal_cals += float(ingredient.group(2))
            meal_fat += float(ingredient.group(3))
            meal_carbs += float(ingredient.group(4))
            meal_protein += float(ingredient.group(5))

                
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
                        "calories": meal_cals,
                        "macros": {"protein": meal_protein, "carbs": meal_carbs, "fat": meal_fat},
                        "ingredients": ingredients,
                        "directions" : directions
                    }

        plan.append(mealObject)

    print(plan)

    return mealplan

