import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting

def generate():
    vertexai.init(project="golden-context-430621-t6", location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-001")

    # Provide some content for the model to generate responses based on
    contents = [
        """
                    System Message:

                    You are a highly professional AI operating in a production environment where accuracy, reliability, and clarity are essential. Your role is to assist users in generating a detailed and precise one-week healthy meal plan, along with a list of all necessary ingredients. The user is depending on your expertise to provide the following:
                    Do not give an other details except the ones explicitly listed. Make sure everything is python format so it can be run through jsonify. 
                    Task Breakdown:
                    List of Ingredients:

                    Generate a comprehensive list of ingredients required for the entire week’s meal plan.
                    Ensure the ingredients are optimized for minimal waste and can be reused across meals.
                    Provide clear portion sizes based on a single person’s daily intake.
                    Meal Plan for One Week:

                    Create a balanced meal plan covering breakfast, lunch, dinner, and snacks for seven days.
                    Each meal should prioritize healthy nutrition, emphasizing:
                    High protein
                    Plenty of vegetables
                    Low processed sugars and refined carbohydrates
                    A good balance of healthy fats, fibers, vitamins, and minerals
                    Ensure the meal plan provides variety across the week to avoid repetition.
                    Nutritional Information:

                    For each meal, provide a detailed nutritional breakdown including:
                    Calories
                    Protein
                    Carbohydrates
                    Fats (specify healthy fats vs. saturated fats)
                    Fiber content
                    Vitamins and minerals where relevant



        """
    ]

    responses = model.generate_content(
        contents,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    response_to_return = ""
    for response in responses:
        response_to_return += response.text
    return response_to_return

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
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