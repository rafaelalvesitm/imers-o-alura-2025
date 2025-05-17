from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)
from datetime import date
import warnings
import os

warnings.filterwarnings("ignore")

# Variáveis globais
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Verifica se a variável de ambiente GOOGLE_API_KEY está definida
if not GOOGLE_API_KEY:
    print("Erro: Variável de ambiente GOOGLE_API_KEY não definida!")
    exit(1)

# --- Definição dos Agentes ---

# Agente Classificador (mantido igual)
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
    return classificacao.strip() # Remove espaços em branco extras

# Agentes Especializados (Exemplos)

def agente_duvida_teorica():
    return Agent(
        name="agente_teorica",
        model="gemini-2.0-flash",
        instruction="""
        Você é um assistente que conhece Python a fundo chamado "Pythonista Teórico".
        Sua tarefa é explicar conceitos de programação, algoritmos e recursos da linguagem Python de forma clara e didática.
        Responda à pergunta focando nos aspectos teóricos e conceituais. 
        De exemplos práticos quando necessário, mas mantenha o foco na teoria.
        Se o usuário pedir para explicar um conceito de programação, forneça uma explicação clara e concisa.
        """,
        description="Agente que responde a dúvidas teóricas sobre algoritmos e Python."
    )

def agente_duvida_codigo():
    return Agent(
        name="agente_codigo",
        model="gemini-2.0-flash",
        instruction="""
        Você é um assistente especializado em Código Python chamado de 'Pythonista Prático'.
        Sua tarefa é ajudar o usuário com dúvidas sobre sintaxe, erros comuns, depuração e boas práticas de codificação em Python.
        Analise o código fornecido (se houver) ou a descrição do problema e ofereça soluções ou explicações relacionadas ao código.
        Responda de forma a ajudar o aluno a entender o problema e a solução. Não forneça apenas o código, mas explique o que ele faz e como funciona.
        Se o código não estiver claro, peça mais informações ou detalhes sobre o que o usuário está tentando fazer.
        Se o usuário fornecer um erro específico, ajude a depurá-lo e a entender o que está acontecendo.
        Se o usuário pedir para explicar um conceito de programação, forneça uma explicação clara e concisa.
        Se o usuário pedir para otimizar um código, forneça sugestões de melhorias e explique por que essas mudanças são benéficas.
        Se o usuário pedir para implementar uma função ou algoritmo específico, forneça um exemplo de código e explique como ele funciona.
        Se o usuário pedir para comparar diferentes abordagens ou bibliotecas, forneça uma análise comparativa e explique as vantagens e desvantagens de cada uma.
        Se o usuário pedir para explicar um erro específico, forneça uma explicação clara e ajude a depurá-lo.
        Se a pergunta não estiver relacionada a código, informe que você, só pode ajudar com questões de programação.
        """,
        description="Agente que responde a dúvidas sobre código em Python, auxiliando o aluno a entender o problema e a solução."
    )

def agente_duvida_disciplina():
    return Agent(
        name="agente_disciplina",
        model="gemini-2.0-flash",
        instruction="""
        Você é um assistente especializado na disciplina 'Fundamentos de Algoritmos'.
        Sua tarefa é fornecer informações gerais sobre a disciplina, como ementa, objetivos, pré-requisitos e estrutura do curso (se disponível em sua base de conhecimento).
        Evite dar detalhes específicos que mudam a cada semestre, a menos que tenha acesso a informações atualizadas.
        """,
        description="Agente que responde a dúvidas gerais sobre a disciplina."
    )

# ... adicione funções para criar outros agentes especializados conforme necessário ...
# def agente_duvida_prova(): ...
# def agente_duvida_professor(): ...
# etc.

def agente_fallback():
    return Agent(
        name="agente_fallback",
        model="gemini-2.0-flash",
        instruction="""
        Você é um assistente geral para a disciplina de Fundamentos de Algoritmos.
        A pergunta feita não se encaixou em nenhuma das categorias especializadas ou está fora do escopo esperado.
        Peça desculpas por não poder responder diretamente ou sugira que o usuário reformule a pergunta.
        """,
        description="Agente de fallback para perguntas não classificadas ou fora do escopo."
    )


# --- Função auxiliar para chamar agente (mantida igual) ---
def chamar_agente(agent: Agent, message_text: str) -> str:
    # Cria um serviço de sessão em memória
    session_service = InMemorySessionService()
    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
    # Nota: Criar uma nova sessão para CADA chamada pode não manter contexto entre chamadas
    # Para manter contexto, você reutilizaria a sessão ou passaria histórico.
    # Para este exemplo simples de dispatcher, uma nova sessão é OK.
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
    return final_response.strip() # Remove espaços/linhas extras no final


# --- Lógica Principal ---
def main():
    print("Bem vindo ao 🤖 BOT Auxiliar sobre a Disciplina de Fundamentos de Algoritmos!")
    print()

    # --- Obter o Tópico do Usuário ---
    topico = input("❓ Faça a sua pergunta: ")

    if not topico:
        print("Você esqueceu de digitar a pergunta!")
        return # Sai da função main se não houver pergunta

    print(f"Maravilha, vamos chamar os nossos agentes 🤖🤖🤖 para te ajudar com essa pergunta!")

    # 1. Classificar a pergunta
    classificacao = agente_classificador(topico)
    print(f"\n--- Debug Classificação: {classificacao} ---\n")

    # 2. Mapear a classificação para o agente correto
    agentes_disponiveis = {
        "Dúvida teórica": agente_duvida_teorica(),
        "Dúvida sobre código em Python": agente_duvida_codigo(),
        "Dúvida sobre a disciplina": agente_duvida_disciplina(),
        # Adicione aqui os outros mapeamentos quando criar os agentes
        # "Dúvida sobre a prova": agente_duvida_prova(),
        # "Dúvida sobre o professor": agente_duvida_professor(),
        # etc.
        "Nenhuma das opções acima": agente_fallback() # Agente padrão para o fallback do classificador
    }

    # Seleciona o agente com base na classificação.
    # Usa .get() para retornar o agente_fallback se a classificação não estiver no dicionário.
    agente_selecionado = agentes_disponiveis.get(classificacao, agente_fallback())

    print(f"--- 🤖 Chamando o Agente Específico: {agente_selecionado.name} ---\n")

    # 3. Chamar o agente selecionado com a pergunta original
    resposta_final = chamar_agente(agente_selecionado, topico)

    print("\n--- ✅ Resposta Final ---\n")
    print(resposta_final)
    print("--------------------------------------------------------------")


if __name__ == "__main__":
    main()