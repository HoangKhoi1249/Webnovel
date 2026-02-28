import json
import google.generativeai as genai
import os




def translate(content, key, model, novel_name):

    """Translate text content using Google's Generative AI model.

    Args:
        content (str): The text content to be translated to Vietnamese.

    Returns:
        str: The translated Vietnamese text.

    Example:
        >>> text = "Hello world"
        >>> result = translate(text)
        >>> print(result)
        "Xin chào thế giới"

    Notes:
        - Requires config.json with api_key, model and novel_name
        - Uses relationship.md file from novel folder for context
        - Uses prompt.txt for translation instructions
        - Temperature and top_p parameters control translation creativity
    """

    os.environ["GRPC_VERBOSITY"] = "ERROR"
    os.environ["GRPC_LOG_SEVERITY"] = "ERROR"


    

    

    # Construct paths for additional files
    novel_folder = f"./novels/{novel_name}/"
    relationship = novel_folder + "relationship.md"

    # Check if relationship file exists
    if not os.path.exists(relationship):
        with open(relationship, 'w', encoding='utf-8') as file:
            pass
    # Load character relationships for context

    with open(relationship, 'r', encoding='utf-8') as file:
        data_relationship = file.read()
    
    # Load translation prompt instructions
    with open("prompt.md", 'r', encoding='utf-8') as file:
        prompt = file.read()

    # Set up model with API key and instructions
    instruc_relate = data_relationship
    genai.configure(api_key=key) # type: ignore

    # Initialize the generative model with system instructions
    model = genai.GenerativeModel( # type: ignore
        model_name=model,
        system_instruction=f"""
        {prompt}
        Đây là thông tin bổ sung:
        {instruc_relate}
    """
        )
    
    # Generate the translated content
    response = model.generate_content(
       contents=f"""
        Dịch văn bản sau sang Tiếng việt:\n
        
        {content}
""",
        generation_config={  # type: ignore
        "temperature": 0.7,
        "top_p": 0.8,
    })

    return response.text

