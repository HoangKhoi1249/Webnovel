import json
import google.generativeai as genai

# Load components from JSON

def translate(content):
    with open('config.json', 'r', encoding="UTF-8") as file:
        data_config = json.load(file)
        key = data_config['api_key']
        model = data_config['model']
        novel_name = data_config['novel_name']

    novel_folder = f"./novels/{novel_name}/"
    relationship = novel_folder + "relationship.md"

    with open(relationship, 'r', encoding='utf-8') as file:
        data_relationship = file.read()
    
    with open("prompt.txt", 'r', encoding='utf-8') as file:
        prompt = file.read()

    instruc_relate = data_relationship

    # Initialize the GenAI client

    genai.configure(api_key=key)

    model = genai.GenerativeModel(
        model_name=model,
        system_instruction=f"""
        {prompt}
        Here is the relationship data:
        {instruc_relate}
    """
        )
    print(prompt, instruc_relate)
    response = model.generate_content(
       contents=f"""
        Translate the following content to Vietnamese:\n
        
        {content}
""",
        generation_config={
        "temperature": 0.7,
        "top_p": 0.8,
    }

    )

    return response.text
