import os
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from ConverterCotacao import obter_cotacao_moeda
from langchain_cohere import ChatCohere
from langchain_cohere import CohereEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import json

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["COHERE_API_KEY"] = "WzrZX6sS5WjRsjxOg92GJz5p6vrhjPiXmss5Z0gn"

llm = ChatCohere(model="command-r-plus")
prompt = hub.pull("rlm/rag-prompt")
def getCotacao(question):
    # Define state for application
    class State(TypedDict):
        question: str
        context: List[Document]
        answer: str

    # Define application steps
    def retrieve(state: State):
        messages = prompt.invoke({"question": state["question"]+". Se passe por um funcionário do Banco Pine. A sua resposta deve retornar o que o usuário quer converter. Por exemplo, se o usuário disser de dólares para reais, a resposta é 'USDBRL'. Se for de ienes para dólares, é a sigla do iene com dólar, ou seja, 'USDJPY'. Retorne somente essa sigla que significa a cotação de uma moeda e de outra, na forma 'MOEDA1MOEDA2' com as siglas das respectivas moedas. Retorne somente isso. \n Exemplos de perguntas: (1) Dólares para reais (2) Ienes para reais. (3) Cotação do dólar (4) Reais para ienes \n Exemplos de respostas: (1) USDBRL (2) JPYBRL (3) USDBRL (4) BRLJPY", "context": ""})
        response = llm.invoke(messages)
        print(response.content)
        cotacao = obter_cotacao_moeda(response.content+"=X")
        return {"context": cotacao}


    def generate(state: State):
        print(state["context"])
        messages = prompt.invoke({"question": state["question"]+". Se passe por um funcionário do Banco Pine. Com base no contexto fornecido, informe a cotação em tempo real da ação. Caso não tenha um bom contexto, diga para o usuário tentar novamente com perguntas mais claras.", "context": state["context"]})
        response = llm.invoke(messages)
        return {"answer": response.content}


    # Compile application and test
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()


    result = graph.invoke({"question": question})
    return result
