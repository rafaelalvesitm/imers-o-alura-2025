import os
from google import genai

def listar_modelos():
    """
    Lista os modelos disponíveis na API do Google GenAI.
    """
    chave_api = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=chave_api)

    for model in client.models.list():
        print(f"Modelo: {model.name} - {model.supported_actions}")
    
if __name__ == "__main__":
    listar_modelos()