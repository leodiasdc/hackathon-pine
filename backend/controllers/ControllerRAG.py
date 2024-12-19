import os
from langchain import hub
from langchain_cohere import ChatCohere
from controllers.RAGCotacao import getCotacao
from controllers.GenerateResponse import getResponse
from config import COHERE_API_KEY
from config import LANGCHAIN_API_KEY 
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY 
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

llm = ChatCohere(model="command-r-plus")
prompt = hub.pull("rlm/rag-prompt")

def getFinalResponse(question):
    initial_message = f"Classifique a seguinte pergunta como 'Sim.' se for 'Cotação de moeda' ou 'Não' se 'Não é cotação de moeda'. Considere que perguntas sobre valores, taxas ou preços de moedas como dólar, euro ou outras moedas estrangeiras são 'Cotação de moeda'. \n Pergunta: {question}. \n Classificação:"
    initial_response = llm.invoke(initial_message)
    if initial_response.content == "Sim.":  
        return getCotacao(question)
    return getResponse(question)
