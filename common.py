api_key = "RGAPI-add2e96d-0208-4b85-86a0-e55477d2b887"


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


# 추가 색상 코드
class ConsoleColor:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BLACK = "\033[30m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    RESET = "\033[0m"
    
    @staticmethod
    def colored(text, color):
        return f"{color}{text}{ConsoleColor.RESET}"

