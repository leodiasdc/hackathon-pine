import os
from langchain import hub
from langchain_cohere import ChatCohere
from RAGCotacao import getCotacao
from GenerateResponse import getResponse

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["COHERE_API_KEY"] = "WzrZX6sS5WjRsjxOg92GJz5p6vrhjPiXmss5Z0gn"

llm = ChatCohere(model="command-r-plus")
prompt = hub.pull("rlm/rag-prompt")

def getFinalResponse(question):
    initial_message = prompt.invoke({"question": question+"\n A pergunta imediatamente anterior é sobre algum dado sobre cotação. Responda somente sim ou não, nada além disso.\n Exemplo de pergunta: Como está o valor do dólar? \n Exemplo de resposta: Sim", "context": ""})
    initial_response = llm.invoke(initial_message)
    print(initial_response)
    if initial_response.content == "Sim.":  
        return getCotacao(question)
    return getResponse(question)

print(getFinalResponse("Como está a cotação do dólar?"))