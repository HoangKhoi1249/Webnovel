import json
import google.generativeai as genai




def translate(content):

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
    # Load configuration from config.json
    with open('config.json', 'r', encoding="UTF-8") as file:
        data_config = json.load(file)
        key = data_config['api_key']
        model = data_config['model']
        novel_name = data_config['novel_name']

    # Construct paths for additional files
    novel_folder = f"./novels/{novel_name}/"
    relationship = novel_folder + "relationship.md"

    # Load character relationships for context

    with open(relationship, 'r', encoding='utf-8') as file:
        data_relationship = file.read()
    
    # Load translation prompt instructions
    with open("prompt.md", 'r', encoding='utf-8') as file:
        prompt = file.read()

    # Set up model with API key and instructions
    instruc_relate = data_relationship
    genai.configure(api_key=key)

    # Initialize the generative model with system instructions
    model = genai.GenerativeModel(
        model_name=model,
        system_instruction=f"""
        {prompt}
        Here is the relationship data:
        {instruc_relate}
    """
        )
    
    # Generate the translated content
    response = model.generate_content(
       contents=f"""
        Dịch văn bản sau sang Tiếng việt:\n
        
        {content}
""",
        generation_config={
        "temperature": 0.7,
        "top_p": 0.8,
    }

    )

    return response.text

