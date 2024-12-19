import os

from langchain import hub
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain.vectorstores import FAISS
from langchain_cohere import ChatCohere
from langchain_cohere import CohereEmbeddings


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["COHERE_API_KEY"] = "WzrZX6sS5WjRsjxOg92GJz5p6vrhjPiXmss5Z0gn"

llm = ChatCohere(model="command-r-plus")
embeddings = CohereEmbeddings(model="embed-english-v3.0")

'''
sites = ["https://www.pine.com","https://www.pine.com/quem-somos/", "https://www.pine.com/para-sua-empresa/credito/","https://www.pine.com/para-sua-empresa/investimentos/", "https://www.pine.com/para-sua-empresa/cambio-e-trade-finance/", "https://www.pine.com/para-sua-empresa/derivativos/", "https://www.pine.com/para-sua-empresa/mercado-de-capitais/", "https://www.pine.com/para-sua-empresa/seguros/", "https://www.pine.com/para-voce/emprestimos/", "https://www.pine.com/para-voce/cartoes/", "https://www.pine.com/para-voce/investimentos/", "https://www.pine.com/quem-somos/#onde-estamos", "https://www.pine.com/relacao-com-investidores/documentos-regulatorios/atas-e-reunioes/"]
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Lista para armazenar todos os documentos
all_documents = []

# Processar os sites e adicionar documentos ao VectorStore
for site in sites:
    loader = WebBaseLoader(site)
    docs = loader.load()
    all_splits = text_splitter.split_documents(docs)
    all_documents.extend(all_splits)

# Criar o FAISS VectorStore e salvar
vector_store = FAISS.from_documents(all_documents, embeddings)
vector_store.save_local("dados_site")
'''

def getResponse(question):
    vector_store = FAISS.load_local(
        "dados_site",
        embeddings,
        allow_dangerous_deserialization=True
    )

    # Define prompt for question-answering
    prompt = hub.pull("rlm/rag-prompt")

    # Define state for application
    class State(TypedDict):
        question: str
        context: List[Document]
        answer: str


    # Define application steps
    def retrieve(state: State):
        retrieved_docs = vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs}


    def generate(state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({"question": state["question"]+"Se passe por um funcionário do Banco Pine. A sua resposta deve ser longa, não precisa responder de forma curta.", "context": docs_content})
        print(messages)
        response = llm.invoke(messages)
        return {"answer": response.content}


    # Compile application and test
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    result = graph.invoke({"question": question})
    return result