import os
from langchain_cohere import ChatCohere
from config import COHERE_API_KEY
from config import LANGCHAIN_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

llm = ChatCohere(model="command-r-plus")

def getTitle(question):
    message = 'Primeira mensagem:'+question+'\n Você deve gerar um título curto com base na primeira mensagem que o usuário começar uma conversa. Certifique-se de que não tenha mais de 40 caracteres. O título deve ser um resumo da mensagem do usuário. Não use aspas nem dois-pontos. Lembre-se que você é o ChatBot do Banco Pine, o PineBot, que está auxiliando um cliente em suas tarefas e respondendo perguntas sobre a empresa.'
    title = llm.invoke(message)
    return title.content
