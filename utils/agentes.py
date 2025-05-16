
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types  # Para criar conteúdos (Content e Part)

# Função auxiliar que envia uma mensagem para um agente via Runner e retorna a resposta final
def chamar_agente(agent: Agent, message_text: str) -> str:
    # Cria um serviço de sessão em memória
    session_service = InMemorySessionService()
    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    # Cria um Runner para o agente
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    # Cria o conteúdo da mensagem de entrada
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    # Itera assincronamente pelos eventos retornados durante a execução do agente
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response

def agente_buscador(topico, data_de_hoje):
    buscador = Agent(
        name="agente_buscador",
        model="gemini-2.0-flash",
        instruction="""
        Você é um assistente de pesquisa. A sua tarefa é usar a ferramenta de busca do google (google_search)
        para recuperar as últimas notícias de lançamentos muito relevantes sobre o tópico abaixo.
        Foque em no máximo 5 lançamentos relevantes, com base na quantidade e entusiasmo das notícias sobre ele.
        Se um tema tiver poucas notícias ou reações entusiasmadas, é possível que ele não seja tão relevante assim
        e pode ser substituído por outro que tenha mais.
        Esses lançamentos relevantes devem ser atuais, de no máximo um mês antes da data de hoje.
        """,
        description="Agente que busca informações no Google",
        tools=[google_search]
    )

    entrada_do_agente_buscador = f"Tópico: {topico}\nData de hoje: {data_de_hoje}"

    lancamentos = chamar_agente(buscador, entrada_do_agente_buscador)
    return lancamentos
  
def agente_classificador(pergunta):
    classificador = Agent(
        name="agente_classificador",
        model="gemini-2.0-flash",
        instruction="""
        Você é um assistente de classificação para auxiliar o professor da disciplina de Fundamentos de Algoritmos dada em Python.  
        A sua tarefa é classificar a pergunta dada conforme as seguintes categorias:
        1. Dúvida sobre a prova: Pergunta relacionada a provas, questões ou avaliações da disciplina.	
        2. Dúvida sobre o professor: Pergunta relacionada ao professor, como horários de atendimento ou preferências de ensino.
        3. Dúvida sobre o curso: Pergunta relacionada ao curso, como requisitos ou estrutura curricular.
        4. Dúvida sobre a disciplina: Pergunta relacionada a disciplina, como pré-requisitos ou conteúdo programático.
        5. Dúvida sobre o material: Pergunta relacionada ao material didático, como livros ou apostilas recomendadas.
        6. Dúvida sobre o laboratório: Pergunta relacionada ao laboratório, como horários ou equipamentos disponíveis.
        7. Dúvida sobre o Projeto: Pergunta relacionada ao projeto, como requisitos ou prazos.
        8. Dúvida teórica: Pergunta sobre conceitos sobre Python. 
        9. Dúvida sobre código em Python: Pergunta relacionada a código em Python, como sintaxe, erros, boas práticas ou bibliotecas.
        
        Responda apenas com a categoria correspondente à pergunta.
        Se a pergunta não se encaixar em nenhuma das categorias acima, responda com "Nenhuma das opções acima".
        Se a pergunta não for relacionada à disciplina de Fundamentos de Algoritmos ou programação em geral, responda com "Nenhuma das opções acima".
        """,
        description="Agente que classifica perguntas em diferentes categorias",
    )

    entrada_do_agente_classificador = f"Texto: {pergunta}"

    classificacao = chamar_agente(classificador, entrada_do_agente_classificador)
    return classificacao