import vertexai
from vertexai.preview.generative_models import GenerativeModel, Tool, grounding, SafetySetting
import google.generativeai as genai
import os

from food_db import search_food_db
from websearch_cheap import search

genai.configure(api_key=os.environ["API_KEY"])

gemini = genai.GenerativeModel("gemini-1.5-flash")



def generate(data=None):

    # Select model
    vertexai.init(project="golden-context-430621-t6", location="us-central1")
    vertex = GenerativeModel("gemini-1.5-flash-001") #used for more accurate responses that need grounding

    genai.configure(api_key=os.environ["API_KEY"])
    gemini = genai.GenerativeModel("gemini-1.5-flash") #used to make more than 5 calls per minute


    
    # Initialize grounding tool, uses datastore in Cloud Code
    tool = Tool.from_retrieval(
    grounding.Retrieval(
        grounding.VertexAISearch(
            datastore='nutrition-information_1727548015090',
            project='golden-context-430621-t6',
            location='global',
        )
    )
    )

    # Initialize grounding tool, uses Google Search Results
    tool2 = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())

    # Configure Generation settings
    generation_config = {
        "max_output_tokens": 8192,

        #degree of randomness in token selection
        "temperature": 1,

        #Tokens are selected from the most (see top-K) to least probable until the sum of their probabilities equals the top-P value
        "top_p": 0.1,

        #Specify a lower value for less random responses
        "top_k": 1
    }

    # Configure safety settings
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

    # Gather nutritional info

    ##  calories
    calories = data['target_calories']

    ##  macros
    carbs = data['macros']['carbs']
    fat = data['macros']['fat']
    protein = data['macros']['protein']

    ##  diet type
    diet_type = data['diet_type']
   
    prompts = [         
                        f"""
                            Please come up with a list of 30 healthy foods to be used in {diet_type} diet.
                            The foods should be fairly common and simple. 
                            Return the output as a comma seperated list of foods and nothing else. 
                            Please make the foods specific, it should ideally be one word.

                        """,
                        """
                                        Please return the best variation of the following foods to be used in a mealplan.
                                        Your output should only contain the best variation.
                                        Example output:
                                            (3042, 'Beef, raw, 90% lean meat / 10% fat, ground', '100 g', 176, '10g', '20.00 g', '0.00 g')
                                        Do not include newlines in your output.\n
                        """,
                        """
                        Please return the nutritional information for the following food, using the following search results.
                        Example output:
                            (Null, ,<insert name of food>, <serving size>, <calories>, <fat>, <protein>, <carbs>)\n
                        """,
                        f"""
                        Using the following foods and their nutritional values, please construct a 1 day meal plan,
                            {calories} calories, {fat} grams of fat, {protein} grams of protein, and {carbs} grams of carbs eaten each day using the foods provided.
                            The following foods are formatted in this way:
                                (<ID>, <Name>, <Serving size>, <calories>, <fat>, <protein>, <carbs>)
                            The meal plan doesnt need to include the ID or the entire name
                            Feel free to adjust the serving size to fulfill the nutritional goals
                            It is of utmost importance that the provided food's nutritional facts add up to match the daily requirement supplied earlier
                        """,
                        f"""
                            Do the the provided food's nutritional facts add up to match the daily requirements supplied? 
                            If not:
                            1) Please make corrections accordingly to ensure that this mealplan meets the daily requirements in a sensible manner
                            2) Return the adjusted mealplan in the same format\n
                        """,


    ]
    
    # Get list of foods to be used
    prompt = prompts
    response = vertex.generate_content(
        prompt[0],
        generation_config= generation_config,
        safety_settings = safety_settings,
        stream=False
    )

    # Split foods into array
    foods = response.text.split(", ")
    print(foods)
    final_food_data = ''

    #For each food, get nutritional information
    for food in foods:
        ## search DB for food
        food_data_array = search_food_db(food)
        food_data_string = "\n".join(str(x) for x in food_data_array)

        ## if DB does not have food, search on web 
        ## FIX ME: Improve Web Scraping
        if len(food_data_string) == 0:
            continue
            ##prompt = prompts[2] + f"Food = {food}\n"
            ##food_data_string = search("Macros and calories of"+food)
        else:
            prompt = prompts[1]

        ## prompts Geminin to choose best food to use from provided data (db or web)
        food_choice = gemini.generate_content(
            prompt + food_data_string,
            generation_config= generation_config,
            stream=False
        )
        
        ## formatting for debug output
        final_food_data += food_choice.text+'<br>'
    
    # Craft Mealplan 
    prompt = prompts[3]
    meal_plan = vertex.generate_content(
            prompt + final_food_data,
            generation_config= generation_config,
            stream=False
        )

    # Check mealplan
    prompt = prompts[4]
    refined_meal_plan = vertex.generate_content(
            prompt + meal_plan.text,
            generation_config= generation_config,
            stream=False
        )
    return refined_meal_plan.text




    # **Used for troubleshooting web search**

    '''
    ## Isolated Web Test ##
    food = 'Quinoa'
    final_food_data = ''

    prompt = prompts[2] + f"Food = {food}\n"
    food_data_string = search("Macros and calories of"+food)

    response = model2.generate_content(
            prompt + food_data_string,
            generation_config= generation_config,
            stream=False
        )
    
    final_food_data += response.text+'<br>'


    return final_food_data
    '''

