import requests

def check_ollama_alive():
    try:
        res = requests.get("http://localhost:11434")
        if res.status_code == 200:
            print("ollama active")
            return True
        else:
            print("ollama does not response")
            return False
    except:
        print("ollama does not work")
        return False
