# 📚 AI Bot Auxiliar para Fundamentos de Algoritmos

Este repositório contém o código-fonte do projeto desenvolvido durante a Imersão IA Alura + Google em 2025. O projeto consiste em um sistema de múltiplos agentes alimentado por modelos Google Gemini, projetado para auxiliar estudantes da disciplina de "Fundamentos de Algoritmos" com suas dúvidas.
O bot atua como um assistente inteligente, capaz de classificar as perguntas dos usuários e direcioná-las para agentes especializados, que utilizam documentos da disciplina (como slides de aula e informações sobre professores) para fornecer respostas precisas e contextuais.

Veja o vídeo explicativo abaixo:

![](https://www.youtube.com/watch?v=WhtcNR-GD2U)

O projeto está disponível no Google Colab em https://colab.research.google.com/drive/1MPPa-HC3vDyyC5obq0VaE24wCiZJXlUv?usp=sharing

# ✨ Funcionalidades

- **Classificação de Perguntas:** Um agente especializado classifica as perguntas dos usuários em categorias predefinidas (prova, professor, disciplina, material, laboratório, projeto, teoria, código Python, etc.).
- **Agentes Especializados:** Diferentes agentes são acionados com base na classificação da pergunta, cada um otimizado para responder a um tipo específico de dúvida.
- **Recuperação Aumentada de Geração (RAG):** Agentes relevantes utilizam conteúdo extraído de documentos PDF da disciplina (aulas e informações do professor) para fundamentar suas respostas, garantindo que as informações sejam precisas e alinhadas com o material do curso.
- **Suporte a Dúvidas Teóricas e Práticas:** Inclui agentes dedicados a explicar conceitos teóricos de programação/algoritmos e a auxiliar com código Python (sintaxe, erros, boas práticas).
- **Extração de Conteúdo de PDF:** Ferramentas para extrair texto de arquivos PDF e armazená-lo em formato JSON para ser utilizado pelos agentes que consultam documentos.
- **Sistema de Fallback:** Um agente de fallback para lidar com perguntas que não se encaixam nas categorias ou estão fora do escopo.

# 🚀 Tecnologias Utilizadas

- **Python:** Linguagem de programação principal.
- **Google Agent Development Kit (ADK):** Framework para construção de sistemas de agentes.[1],[2]
- **Google Gemini Models:** Modelos de linguagem utilizados pelos agentes (ex: gemini-2.0-flash).[3]
- **PyMuPDF (fitz):** Biblioteca para extração de texto de arquivos PDF.
- **JSON:** Formato para armazenamento de dados extraídos dos PDFs.
- **python-dotenv (não utilizado diretamente no código Colab, mas recomendado para ambiente local):** Para gerenciar variáveis de ambiente (como a API Key).
- **Google Colab:** Ambiente de desenvolvimento utilizado no projeto original.

# ⚙️ Configuração e Instalação

Este projeto foi desenvolvido inicialmente no Google Colab. Para acessar o Google Colab use o link https://colab.research.google.com/drive/1MPPa-HC3vDyyC5obq0VaE24wCiZJXlUv?usp=sharing


Para executá-lo em um ambiente local, siga os passos abaixo:

1. Clone este repositório

Clone este repositório para o seu ambiente local. 

2. Instale as dependencias. 

Recomendo usar um ambiente virtual para isso. Use o seguinte comando:

Instale as dependências  Recomendo usar um ambiente virtual.

```bash
python -m venv venv
pip install -r requirements.txt
```

3. Coloque a sua chave de API em um arquivo `.env`

Crie um arquivo `.env` na pasta raiz do projeto e escreva `GOOGLE_API_KEY="<sua chave de api>"`. 

4. Prepare os documentos da disciplina e do professor. 

Por motivos de privacidade não estou disponibilizando os arquivos da disciplina e do professor, sendo assim inclua tais arquivos nas pastas `aulas` e `professor` deste projeto. Coloque os arquivos PDF relevantes (slides de aula, currículo do professor) dentro dessas pastas. O código espera encontrar arquivos PDF nessas localizações para a extração de texto.

# ▶️ Como Executar

Após configurar o ambiente e preparar os documentos, execute o script principal:

```bash
python projeto.py
```
O script irá:

Extrair o texto dos PDFs nas pastas ./aulas e ./professor e salvá-lo em arquivos JSON (aulas.json e professores.json).
Iniciar o loop de interação com o usuário, solicitando perguntas.
Classificar cada pergunta e chamar o agente apropriado para gerar a resposta.

# 📁 Estrutura do Projeto (Sugestão)
.
├── aulas/
│   ├── aula1.pdf (Não divulgado)
│   ├── aula2.pdf (Não divulgado)
│   └── ...
├── professor/
│   └── professor.pdf (Não divulgado)
├── aulas.json (Não divulgado e criado após a primeira execução)
├── professores.json (Não divulgado e criado após a primeira execução)
├── projeto.py  # Arquivo principal com o código
├── README.md      # Este arquivo
└── requirements.txt # Dependências
Use code with caution.

# 🤝 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues para relatar bugs ou sugerir melhorias, ou enviar Pull Requests com suas implementações.

# 📄 Licença

Este projeto está sob a licença [Escolha uma Licença, ex: MIT]. Veja o arquivo LICENSE para mais detalhes.

# 🙏 Agradecimentos

Este projeto foi desenvolvido como parte da Imersão IA promovida pela Alura em parceria com o Google em 2025. Agradecemos a oportunidade de aprender e aplicar conceitos de Inteligência Artificial e sistemas multi-agentes.