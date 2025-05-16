# Full example code for the basic capital agent
# --- Full example code demonstrating LlmAgent with Tools vs. Output Schema ---
import json # Needed for pretty printing dicts
import asyncio

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel, Field

# --- 1. Define as constantes ---
APP_NAME = "AgenteIntecao"
USER_ID = "usuario"
SESSION_ID = "session_tool_agent"
MODEL_NAME = "gemini-2.0-flash"

# --- 2. Define os agentes ---

# Agente de intenção 
agente_intencao = Agent(
    model=MODEL_NAME,
    name="agente_intencao",
    description="Classifica a inteção do usuário em dúvida teórica, duvida de código ou novo exercício para a disciplina de Fundamentos de Algoritmos.",
    instruction="""Você é um agente de IA que classifica a intenção do usuário.
O usuário pode fazer perguntas sobre teoria, dúvidas de código ou solicitar novos exercícios.
1. Classifique a intenção do usuário em uma das seguintes categorias:
    - dúvida teórica: Perguntas sobre conceitos ou teorias.
    - dúvida de código: Perguntas sobre problemas específicos de código Python. 
    - novo exercício: Solicitações para criar novos exercícios sobre Fundamentos de Algoritmos.
2. Responda ao usuário com a categoria identificada.
""",
    output_key="intencao_usuario", 
)

# --- 3. Define um executor para o agente ---
session_service = InMemorySessionService()

# Create separate sessions for clarity, though not strictly necessary if context is managed
session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)


# Create a runner for EACH agent
runner = Runner(
    agent=agente_intencao,
    app_name=APP_NAME,
    session_service=session_service
)


# --- 4. Executa o código em questão ---
async def executa_agente(
    runner_instance: Runner,
    agent_instance: Agent,
    session_id: str,
    query: str
):
    user_content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_content = "No final response received."
    async for event in runner_instance.run_async(user_id=USER_ID, session_id=session_id, new_message=user_content):
        print(f"Event: {event.content}, Author: {event.author}") # Uncomment for detailed logging
        if event.is_final_response() and event.content and event.content.parts:
            # For output_schema, the content is the JSON string itself
            final_response_content = event.content.parts[0].text

    print(f"{final_response_content}")

# --- testando ---
async def main():
    texto = input("Digite o seu prompt: ")
    await executa_agente(runner, agente_intencao, SESSION_ID, texto)

if __name__ == "__main__":
    asyncio.run(main())