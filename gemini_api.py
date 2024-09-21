import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting

def generate():
    vertexai.init(project="golden-context-430621-t6", location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-001")

    # Provide some content for the model to generate responses based on
    contents = [
                        """
                                    System Message:
                                    Tell me a great story




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
    #degree of randomness in token selection
    "temperature": 1,
    #Tokens are selected from the most (see top-K) to least probable until the sum of their probabilities equals the top-P value
    "top_p": 0.1,
    #Specify a lower value for less random responses
    "top_k": 2
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