import os
from langchain import hub
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

from langchain_cohere import ChatCohere
from langchain_cohere import CohereEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.messages.human import HumanMessage
import yfinance

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["COHERE_API_KEY"] = "PQwXr6lzvXD8iVe9qN76Nj8Qa3OMLGlx838symV9"

llm = ChatCohere(model="command-r-plus")
embeddings = CohereEmbeddings(model="embed-english-v3.0")
vector_store = InMemoryVectorStore(embeddings)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Define prompt for question-answering
# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

messages =[HumanMessage(content=f"Você é um assistente virtual para identificar qual ação e qual dia o usuário selecionou. Sua reposta deve ser apenas uma mensagem em formato json indicando a cotação com a chave 'cotacao' e a data com a chave 'date'. O tipo de cotação (dólar, libra, etc), não o valor,  ou a sigla da ação (BBAS3, etc) deve ser a resposta. A data deve estar formatada como Dia/Mês/Ano.\nQuestão: Como está a cotação da moeda americana no dia 16/12/2023? \nResposta:", additional_kwargs={}, response_metadata={})]
print(messages)
response = llm.invoke(messages)
print(response)
'''
# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages =[HumanMessage(content=f"Você é um assistente virtual para identificar qual ação e qual dia o usuário selecionou. Sua reposta deve ser apenas a cotação (dólar, libra, etc) ou a sigla da ação (BBAS3, etc) e o dia que a pessoa perguntou sobre.\nQuestion: Como estava a cotação do dólar no dia 16/12/2023? \nContext: {docs_content}  \nAnswer:", additional_kwargs={}, response_metadata={})]
    print(messages)
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

result = graph.invoke({"question": "O que é o Banco Pine?"})
print(result['answer'])
'''