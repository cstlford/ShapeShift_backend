from openai import OpenAI
import time
import re
client = OpenAI()

def calculate(nutrient,output):
    sum = 0
    match nutrient:
        case "calories":
            regex = "(\d{1,4})( cals)"
        case _:
            regex = "(\d{1,4})(g "+nutrient+")"
    amounts = re.findall(regex, output)
    for amount in amounts:
        sum += int(amount[0])

    return sum


def check(output, calories, fat, carbs, protein):

    fat = int(re.search(r"\d{1,4}", fat).group())
    carbs = int(re.search(r"\d{1,4}", carbs).group())
    protein = int(re.search(r"\d{1,4}", protein).group())

    gen_calories = calculate("calories",output)
    gen_fat = calculate("fat",output)
    gen_carbs = calculate("carbs",output)
    gen_protein = calculate("protein",output)
    
    print(
        f'''
        Start {calories} => Generated {gen_calories} Error: {abs(calories - gen_calories)/calories}
        Start {fat} => Generated {gen_fat} Error: {abs(fat - gen_fat)/fat}
        Start {carbs} => Generated {gen_carbs} Error: {abs(carbs - gen_carbs)/carbs}
        Start {protein} => Generated {gen_protein} Error: {abs(protein - gen_protein)/protein}
        '''
    )

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
                    Step 1: Find a list of about 20 healthy, diverse foods to be used in a mealplan for a(n) {diet_type} client.
                            The client likes {preference_foods} and will not eat {avoid_foods}

                    Step 2: Gather nutritional information for each food found in the 1st step corresponding to its serving size

                    Return the list
                """
            }
        ]
    )

    foodlist = completion.choices[0].message.content
    
    completion1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert nutritionist who builds nutrition plans tailored to your clients specific needs"},
            {
                "role": "user",
                "content":
                
                f"""
                    Step 1: Create a mealplan for a(n) {diet_type} client for {1} day(s) with {3} meals using the following foods and their nutritional information:

                    Foods: 
                        {foodlist}


                    Step 2: After the mealplan has been created, audit the mealplan to fit the following nutritional requirements:
                        Daily Calories: {calories}
                        Daily Carbs: {carbs}
                        Daily Fat: {fat}
                        Daily Protein: {protein}


                    Step 3: Format the output to look like the following sample (there can be more than 2 foods each meal if needed)
                            Include a list of ingredients for the mealplan at the end
           

                    Sample Mealplan:
                        ## Breakfast: <br>
                        - 4 of food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 4 of food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 4 of food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc
                        ## Lunch: <br>
                        - 8 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 2 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc
                        ## Snack: <br>
                        - 2 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc 
                        ## Dinner: <br>
                        - 8 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 2 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        - 2 oz food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc 
                        ## Evening Snack:
                        - 3 food [x cals, [x]g fat, [x]g carbs, [x]g protein] <br>
                        ... etc
                        ### Totals: - Calories: x - Fat: [x]g - Carbs: [x]g - Protein: [x]g <br>
                """
            }
        ]
    )


    output = completion1.choices[0].message.content

    timeEnd = time.time()
    



    #Output needs:
    #Macros
    check(output, calories, fat, carbs, protein)
    #Ingredient list
    ## algorithmic
    #Directions
    ## executed daily, to avoid overload


    return output+"<br>Time to execute: "+str(timeEnd-timeStart)


