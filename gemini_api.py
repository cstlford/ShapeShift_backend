import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting

def generate(data=None):
    vertexai.init(project="golden-context-430621-t6", location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-001")


    #calories
    calories = data['target_calories']

    #macros
    carbs = data['macros']['carbs']
    fat = data['macros']['fat']
    protein = data['macros']['protein']

    # -- TO DO -- #
    #Multi-generation:
    ## First Generation - Randomness is high for model that provides food choices (RAG not needed)
    ## Second Generation - Randomness is decreased for determining the macronutrients/calories needed for each food (RAG Needed) 
    ## Third Generation - Randomness is kept low, model determines which brands to use based off of store preference (RAG Needed)
    ## Fourth Generation - Randomness is kept low, model proofreads the last output

    ##FIX ME - add contents for each generation
    contents = [
                        f"""
                                    System Message:

                                    You are a capable nutrition model being utilized in an API that takes in
                                    the amount of calories a user needs to eat and the macronutrients needed for one day.

                                    Generate a mealplan for 7 days for a user that needs to eat {calories} calories in a day with the following macros: 
                                    {carbs} grams of carbs,
                                    {fat} grams of fat,
                                    {protein} grams protein.

                                    The mealplan will have three meals a day that will list the foods with measurements in grams. 

                                    Each food item in each meal will have the calories and macros listed.

                                    Each meal will have the calories and macros listed, as well as a designation (such as breakfast, lunch, and dinner).

                                    The foods will be healthy, nutrient dense foods.


                        """,

                        f"""
                                    System Message:

                                    You are a capable nutrition model being utilized in an API that takes in
                                    the amount of calories a user needs to eat and the macronutrients needed for one day.

                                    You are reviewing an already complete meal plan for accuracy. 
                                    For each meal, assess the quantity (grams) of each food item and ensure the calorie and macro calculations are correct This is of the utmost priority.
                                    If adjustments are needed, replace the incorrect values with the correct values in the output.
                                    Include ingredients for any food item that does not constitute of a single food
                                    Return the output as follows, where the text in <> is what need to be adjusted, and there is <br> inserted after each header of each level and each bullet point.:
                                    # <insert day here> <br>
                                    ## <insert meal here> <br>
                                    ### <Insert food item here with grams ()> <br>
                                     - macro information <br>
                                     - calorie information <br>
                                     -- ingredient <br>
                                     -- ingredient <br>
                                    
                                    After returning the output with the formatting described above, give a breakdown of the changes you made between the input and output, including the changes you made to the nutritional info.
                                    The breakdown should be an ordered list of changes you made under the heading (level 3) 'Changes'. Here is an example:
                                    ### Changes <br>
                                    - <insert change here> <br>
                                    The input is: \n
                        """,
                        f"""
                                    You are a nutritionist tasked with generating a meal plan. Based on the user details below, create a daily meal plan.

                                    User details:
                                    - Total daily calories: {calories}
                                    - Target macronutrient split: 
                                    - Protein: {protein}
                                    - Carbs: {carbs}
                                    - Fat: {fat}
                                    - Diet: Omnivore
                                    - Preferences: Likes Italian food, dislikes shellfish
                                    - Number of meals per day: 3
                                    - Number of days: 7

                                    For each meal in the day, include the following:
                                    - Title of the meal
                                    - Ingredients with their calories and macronutrient breakdown (protein, carbs, fat) per ingredient
                                    - Directions on how to prepare the meal

                                    Ensure that the total calories and macronutrients for the day match the user's goals. Use common ingredients and keep the preparation simple.
                        """
    ]


    

    ##FIX ME - add 4 generation cycles according to specifications above 

    #generates first response
    responses = model.generate_content(
        contents[0],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    #compiles first response (can probably eliminate)
    first_response = ""
    for response in responses:
        first_response += response.text

    #peer reviews first response
    betterresponses = model.generate_content(
        contents[1] + first_response,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    #compiles second response (can probably eliminate)
    response_to_return = ""
    for response in betterresponses:
        response_to_return += response.text
    return response_to_return

##FIX ME - add generation config block with higher random value
generation_config = {
    "max_output_tokens": 8192,
    #degree of randomness in token selection
    "temperature": 1,
    #Tokens are selected from the most (see top-K) to least probable until the sum of their probabilities equals the top-P value
    "top_p": 0.1,
    #Specify a lower value for less random responses
    "top_k": 1
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]