from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)
from datetime import date
import warnings
import os

# Funções em outros arquivos
from utils.utils import listar_modelos
from utils.agentes import agente_buscador, agente_classificador

warnings.filterwarnings("ignore")

# Variáveis globais
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def main():
    data_de_hoje = date.today().strftime("%d/%m/%Y")

    print("Bem vindo ao BOT Auxiliar sobre a Disciplina de Fundamentos de Algoritmos!")

    # --- Obter o Tópico do Usuário ---
    topico = input("❓ Faça a sua pergunta: ")

    # Inserir lógica do sistema de agentes ################################################
    if not topico:
        print("Você esqueceu de digitar a pergunta!")
    else:
        print(f"Maravilha, vamos classficar a sua pergunta: {topico}")

        lancamentos_buscados = agente_classificador(topico)
        print("\n--- 📝 Resultado do Agente 1 ---\n")
        print(lancamentos_buscados)
        print("--------------------------------------------------------------")

if __name__ == "__main__":
    # Listar os modelos disponíveis. Comentei para não poluir a tela
    # listar_modelos()
    main()