import os
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

from langchain_cohere import ChatCohere
from langchain_cohere import CohereEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
import json

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["COHERE_API_KEY"] = "PQwXr6lzvXD8iVe9qN76Nj8Qa3OMLGlx838symV9"

llm = ChatCohere(model="command-r-plus")
embeddings = CohereEmbeddings(model="embed-english-v3.0")
sites = ["https://www.pine.com","https://www.pine.com/quem-somos/", "https://www.pine.com/para-sua-empresa/credito/","https://www.pine.com/para-sua-empresa/investimentos/", "https://www.pine.com/para-sua-empresa/cambio-e-trade-finance/", "https://www.pine.com/para-sua-empresa/derivativos/", "https://www.pine.com/para-sua-empresa/mercado-de-capitais/", "https://www.pine.com/para-sua-empresa/seguros/", "https://www.pine.com/para-voce/emprestimos/", "https://www.pine.com/para-voce/cartoes/", "https://www.pine.com/para-voce/investimentos/", "https://www.pine.com/quem-somos/#onde-estamos", "https://www.pine.com/relacao-com-investidores/documentos-regulatorios/atas-e-reunioes/"]
vector_store = InMemoryVectorStore(embeddings)
questions = (
    "O que é o Banco Pine?",
    "Qual é o principal objetivo do Banco Pine?",
    "Onde está localizada a sede do Banco Pine?",
    "Quais são os serviços oferecidos pelo Banco Pine?",
    "O Banco Pine atende pessoas físicas ou apenas empresas?",
    "Como abrir uma conta no Banco Pine?",
    "O Banco Pine oferece serviços de crédito para empresas?",
    "Quais são os tipos de crédito disponíveis no Banco Pine?",
    "O que é a linha de crédito para capital de giro do Banco Pine?",
    "Como funciona o crédito para exportação oferecido pelo Banco Pine?",
    "O Banco Pine trabalha com investimentos?",
    "Quais são os produtos de investimento oferecidos pelo Banco Pine?",
    "Como funciona o serviço de câmbio do Banco Pine?",
    "O Banco Pine oferece serviços de seguros?",
    "Quais são os seguros empresariais disponíveis no Banco Pine?",
    "Como entrar em contato com o Banco Pine?",
    "Quais são os benefícios de ser cliente do Banco Pine?",
    "O Banco Pine oferece serviços para pequenas empresas?",
    "Quais são os prazos de crédito do Banco Pine?",
    "Como funciona a fiança bancária no Banco Pine?",
    "O Banco Pine oferece suporte para startups?",
    "O que é a Nota de Crédito à Exportação (NCE)?",
    "Como funciona a Cédula de Produto Rural Financeira (CPR-F)?",
    "Quais são os custos associados aos serviços do Banco Pine?",
    "O Banco Pine oferece consultoria financeira?",
    "Como funciona a gestão de derivativos no Banco Pine?",
    "Quais são as soluções de trade finance do Banco Pine?",
    "O Banco Pine é regulamentado pelo Banco Central?",
    "Como é o processo de concessão de crédito no Banco Pine?",
    "O Banco Pine trabalha com financiamentos imobiliários?",
    "Quais são os setores atendidos pelo Banco Pine?",
    "O Banco Pine oferece serviços de pagamento de fornecedores?",
    "Como funciona a antecipação de recebíveis no Banco Pine?",
    "O Banco Pine oferece linhas de crédito para microempresas?",
    "Quais são as taxas cobradas pelo Banco Pine?",
    "O Banco Pine oferece serviços de private banking?",
    "Como é a experiência de atendimento ao cliente no Banco Pine?",
    "O Banco Pine oferece serviços de financiamento para importação?",
    "Como funciona o serviço de hedge cambial no Banco Pine?",
    "Quais são as políticas de segurança do Banco Pine?",
    "O Banco Pine trabalha com CRAs e CRIs?",
    "Como o Banco Pine apoia empresas no mercado de capitais?",
    "O Banco Pine oferece serviços de consultoria tributária?",
    "Quais são os requisitos para obter crédito no Banco Pine?",
    "Como o Banco Pine gerencia riscos financeiros?",
    "Quais são os benefícios de investir com o Banco Pine?",
    "O Banco Pine oferece serviços para organizações não governamentais?",
    "Quais são as opções de crédito para o setor de agronegócio?",
    "Como funciona a conta garantida no Banco Pine?",
    "Quais são os benefícios do Confirming para empresas?",
    "O Banco Pine oferece soluções para o setor de tecnologia?",
    "Quais são os prazos para operações de câmbio no Banco Pine?",
    "Como o Banco Pine apoia projetos de infraestrutura?",
    "Quais são os serviços de seguros para pessoas físicas?",
    "Como é o processo de emissão de debêntures no Banco Pine?",
    "O Banco Pine oferece serviços para o setor de energia?",
    "Quais são os documentos necessários para abrir uma conta empresarial?",
    "Como funciona o processo de avaliação de crédito no Banco Pine?",
    "Quais são as opções de seguros patrimoniais no Banco Pine?",
    "O Banco Pine oferece serviços de planejamento sucessório?",
    "Quais são os benefícios de contratar uma fiança bancária?",
    "Como o Banco Pine auxilia empresas na emissão de títulos de dívida?",
    "Quais são as taxas associadas à gestão de derivativos?",
    "O Banco Pine oferece soluções financeiras para o setor de saúde?",
    "Quais são as vantagens de utilizar serviços de trade finance?",
    "Como o Banco Pine gerencia suas operações internacionais?",
    "Quais são os benefícios do serviço de câmbio para pessoas físicas?",
    "O Banco Pine oferece serviços de pagamento internacional?",
    "Como é o processo de contratação de seguros empresariais?",
    "Quais são as soluções para o setor de varejo?",
    "Como funciona o serviço de hedge de commodities no Banco Pine?",
    "Quais são as soluções financeiras para o setor automotivo?",
    "O Banco Pine oferece serviços de gestão de caixa?",
    "Quais são os benefícios de trabalhar com o Banco Pine?",
    "Como funciona o serviço de custódia de ativos?",
    "Quais são as taxas cobradas em operações de crédito?",
    "Como o Banco Pine auxilia empresas em fusões e aquisições?",
    "Quais são os produtos de renda fixa oferecidos?",
    "O Banco Pine oferece serviços de leasing?",
    "Como é o suporte para empresas em situações de crise?",
    "Quais são as soluções para empresas do setor de infraestrutura?",
    "O Banco Pine trabalha com crédito rural?",
    "Quais são os benefícios do serviço de financiamento imobiliário?",
    "Como funciona o serviço de gestão de riscos financeiros?",
    "Quais são as soluções de financiamento para startups?",
    "O Banco Pine oferece consultoria para fusões?",
    "Quais são os benefícios dos seguros patrimoniais?",
    "Como funciona o serviço de pagamento de fornecedores?",
    "Quais são os benefícios do serviço de capital de giro?",
    "O Banco Pine oferece soluções para o setor de educação?",
    "Como funciona o serviço de financiamento para equipamentos?",
    "Quais são os benefícios do serviço de financiamento de projetos?",
    "O Banco Pine oferece serviços de consultoria em mercado de capitais?",
    "Quais são os benefícios do serviço de gestão de tesouraria?",
    "Como funciona o serviço de financiamento para importação?",
    "Quais são os benefícios do serviço de financiamento para exportação?",
    "O Banco Pine oferece soluções para o setor de agronegócio?",
    "Quais são os benefícios do serviço de financiamento para startups?",
    "Como funciona o serviço de hedge cambial?",
    "Como funciona o serviço de emissão de debêntures?",
    "Quais são os benefícios do serviço de capital de giro para empresas?",
    "O Banco Pine oferece soluções financeiras para o setor de logística?",
    "Como funciona o serviço de hedge de commodities?",
    "Quais são os benefícios do serviço de antecipação de recebíveis?",
    "O Banco Pine oferece crédito consignado?",
    "Como funciona o serviço de consultoria em derivativos?",
    "Quais são os benefícios do serviço de seguros empresariais?",
    "O Banco Pine oferece soluções para o setor de energia renovável?",
    "Quais são os benefícios do serviço de financiamento para infraestrutura?",
    "Como o Banco Pine apoia empresas em processos de internacionalização?",
    "O Banco Pine oferece serviços de consultoria em fusões e aquisições?",
    "Quais são as vantagens do serviço de financiamento para importação?",
    "O Banco Pine oferece crédito imobiliário para empresas?",
    "Como funciona o serviço de pagamento de fornecedores internacionais?",
    "Quais são as opções de investimento de renda fixa no Banco Pine?",
    "O Banco Pine oferece soluções financeiras para o setor de tecnologia?",
    "Como funciona o serviço de capital de giro rotativo?",
    "Quais são os benefícios do serviço de seguros patrimoniais?",
    "O Banco Pine oferece consultoria em mercado de capitais?",
    "Quais são os benefícios do serviço de trade finance?",
    "Como o Banco Pine apoia startups em crescimento?",
    "Quais são os benefícios do serviço de financiamento de projetos?",
    "Qual é a história do Banco Pine?",
    "Quais são os principais valores do Banco Pine?",
    "Quem são os executivos responsáveis pelo Banco Pine?",
    "Onde estão localizadas as unidades do Banco Pine?",
    "Qual é o foco principal de atuação do Banco Pine?",
    "Quais setores econômicos o Banco Pine atende?",
    "O Banco Pine possui iniciativas de sustentabilidade?",
    "Como o Banco Pine apoia o agronegócio?",
    "Quais são as certificações de segurança e compliance do Banco Pine?",
    "O Banco Pine oferece serviços internacionais?",
    "Quais são as opções de crédito disponíveis para empresas no Banco Pine?",
    "O que é a linha de crédito para capital de giro?",
    "Como funciona o crédito NCE/CCE para empresas exportadoras?",
    "O que é a Nota Comercial oferecida pelo Banco Pine?",
    "Como funciona o crédito Cheque Empresa?",   
    "O que é a linha de crédito Conta Garantida?",                   
    "Quais são os benefícios do crédito garantido pelo FGI do BNDES?",
    "Como o Banco Pine oferece suporte a micro, pequenas e médias empresas?",
    "O que é a CPR Financeira e para quem ela é indicada?",
    "Como funciona o Confirming no Banco Pine?",
    "Quais produtos de investimento o Banco Pine oferece para empresas?",
    "Como funciona o serviço de emissão de debêntures pelo Banco Pine?",
    "O que são CRAs e CRIs, e como o Banco Pine os utiliza?",
    "Como o Banco Pine apoia empresas no mercado de capitais?",
    "Quais são as taxas associadas aos investimentos empresariais no Banco Pine?",
    "Quais serviços de câmbio o Banco Pine oferece?",
    "Como o Banco Pine auxilia empresas em operações de exportação?",
    "O que é o serviço de Trade Finance do Banco Pine?",
    "Como funciona o financiamento de importação no Banco Pine?",
    "O Banco Pine oferece consultoria para operações de câmbio?",
    "Quais são os serviços de gestão de derivativos oferecidos pelo Banco Pine?",
    "Como o Banco Pine auxilia empresas na proteção contra riscos cambiais?",
    "O que é a operação de hedge, e como ela funciona no Banco Pine?",
    "Quais tipos de seguros empresariais o Banco Pine oferece?",
    "Como contratar um seguro empresarial no Banco Pine?",
    "Quais setores podem se beneficiar dos seguros oferecidos pelo Banco Pine?",
    "Quais tipos de empréstimos o Banco Pine oferece para pessoas físicas?",
    "Como funciona o empréstimo consignado no Banco Pine?",
    "O que é a antecipação do saque-aniversário do FGTS?",
    "Quais são os requisitos para solicitar um empréstimo pessoal no Banco Pine?",
    "Quais são os tipos de cartões oferecidos pelo Banco Pine?",
    "O Banco Pine oferece benefícios exclusivos em seus cartões?",
    "Como funciona o programa de recompensas dos cartões do Banco Pine?",
    "O Banco Pine oferece cartões internacionais?",
    "Quais são os limites iniciais dos cartões do Banco Pine?",
    "Como solicitar um aumento de limite no cartão do Banco Pine?",
    "O Banco Pine oferece cartões de crédito sem anuidade?",
    "Como acessar a fatura digital dos cartões do Banco Pine?",
    "Quais são as condições para obtenção de um cartão corporativo?",
    "Quais produtos de investimento estão disponíveis para pessoas físicas no Banco Pine?",
    "O Banco Pine oferece fundos de investimento?",
    "Como funciona o processo de abertura de conta para investimentos?",
    "Quais são os benefícios de investir em CRIs e CRAs pelo Banco Pine?",
    "O Banco Pine oferece suporte para planejamento financeiro pessoal?",
    "Como acessar o extrato de investimentos no Banco Pine?",
    "O Banco Pine oferece aplicativos para dispositivos móveis?",
    "Como funciona o Internet Banking do Banco Pine?",
    "Quais serviços estão disponíveis no app do Banco Pine?",
    "Como recuperar a senha do Internet Banking?",
    "É possível realizar transferências internacionais pelo app do Banco Pine?",
    "Onde encontrar as atas de reuniões do Banco Pine?",
    "Quais são os ratings de crédito do Banco Pine?",
    "Onde acessar os comunicados e documentos regulatórios?",
    "Como receber alertas de RI do Banco Pine?",
    "O Banco Pine divulga informações sobre dividendos?",
    "Quais eventos estão listados no calendário de RI?",
    "Compliance e Regulamentação",
    "O Banco Pine segue quais normativas de compliance?",
    "Quais são os formulários de compliance disponíveis no site do Banco Pine?",
    "Como o Banco Pine garante a proteção de dados dos clientes?",
    "Quais são as políticas de governança do Banco Pine?",
    "O Banco Pine oferece soluções financeiras sob medida para empresas?",
    "Quais setores podem se beneficiar de produtos personalizados do Banco Pine?",
    "Como funciona o atendimento especializado para empresas no Banco Pine?",
    "O Banco Pine oferece suporte para startups?",
    "Como entrar em contato com a central de atendimento do Banco Pine?",
    "O Banco Pine oferece atendimento 24 horas?",
    "Quais são os canais de suporte para dúvidas sobre crédito?",
    "Como agendar uma reunião com um especialista financeiro do Banco Pine?",
    "O Banco Pine oferece suporte em idiomas além do português?",
    "Quais são as soluções do Banco Pine para o setor imobiliário?",
    "Como o Banco Pine apoia empresas de tecnologia?",
    "O Banco Pine oferece suporte para negócios no setor de saúde?",
    "Quais são as opções de crédito para empresas de varejo?",
    "Como o Banco Pine auxilia empresas de logística?",
    "Quais são os serviços de trade finance disponíveis no Banco Pine?",
    "O Banco Pine oferece consultoria para planejamento tributário?",
    "Quais são as taxas médias cobradas em operações de câmbio?",
    "Como funciona a antecipação de recebíveis no Banco Pine?",
    "Quais são os produtos de seguros empresariais mais populares?",
    "O Banco Pine utiliza inteligência artificial em seus serviços?",
    "Quais são as principais inovações tecnológicas do Banco Pine?",
    "O Banco Pine oferece suporte para integração com sistemas de ERP?",
    "Como funciona a API para clientes corporativos do Banco Pine?",
    "O Banco Pine oferece cursos ou conteúdos sobre educação financeira?",
    "Como o Banco Pine ajuda empresas a gerenciar dívidas?",
    "Quais são as dicas do Banco Pine para planejamento financeiro empresarial?",
    "Quais são os horários de funcionamento das agências do Banco Pine?",
    "O Banco Pine possui parcerias com outros bancos ou instituições financeiras?",
    "Como o Banco Pine apoia projetos de responsabilidade social?"
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

for site in sites:
    loader = WebBaseLoader(site)
    docs = loader.load()
    all_splits = text_splitter.split_documents(docs)
    _ = vector_store.add_documents(documents=all_splits)


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

# Criação dos contextos através de perguntas e respostas com RAG
lista_dados = []
'''
for question in questions:
    try:
        result = graph.invoke({"question": question})
        lista_dados.append({"context": str(result["context"]), "question":question, "answer":str(result["answer"])})
    except:
        break
'''
result = graph.invoke({"question": "O que é o Banco Pine?"})
print(result['answer'])
