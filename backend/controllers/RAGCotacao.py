import os
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from controllers.ConverterCotacao import obter_cotacao_moeda
from langchain_cohere import ChatCohere
from langchain_cohere import CohereEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from config import COHERE_API_KEY, LANGCHAIN_API_KEY

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

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
        messages = f"Dado que a pergunta é sobre cotação de moedas, identifique o par de moedas no formato 'MOEDA1MOEDA2'. Um exemplo de resposta seria 'USDBRL'. Use os códigos ISO 4217 das moedas (exemplo: USD para dólar americano, BRL para real brasileiro). Se uma das moedas não for mencionada, assuma que a outra moeda é o real (BRL). Você é um funcionário do Banco Pine, que se chama PineBot (ChatBot com IA). Você é um assistente amigável, que adapta sua linguagem (formal ou informal).  \nPergunta: {question}. Resposta no formato 'MOEDA1MOEDA2':"
        response = llm.invoke(messages)
        print(response.content)
        cotacao = obter_cotacao_moeda(response.content+"=X")
        return {"context": cotacao}


    def generate(state: State):
        print(state["context"])
        messages = prompt.invoke({"question": state["question"]+". Se passe por um funcionário do Banco Pine. Com base no contexto fornecido, informe a cotação em tempo real da ação. Caso não haja um contexto peça para o usuário especificar qual moeda ele quer em relação a cotação de qual moeda", "context": state["context"]})
        response = llm.invoke(messages)
        return {"answer": response.content}


    # Compile application and test
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()


    result = graph.invoke({"question": question})
    print("hello there answer cotação")
    print(type(result['answer']))
    print(result)
    print(result['answer'])
    return result['answer']
