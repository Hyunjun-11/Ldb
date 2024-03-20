api_key = "RGAPI-c9e33aa5-8e38-4fff-ad6b-f936a1ab1bb9"


import json

def load_json(file_name):
    try:
        with open(file_name, "r",encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None
    except Exception as e:
        print(f"Error loading JSON from '{file_name}': {e}")
        return None


