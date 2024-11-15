import os
from dotenv import load_dotenv

import streamlit as st
from client import RiskAzureChatOpenAI 
from client import RiskAzureOpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
import chromadb

api_key = ""
DOC_PATH = "Files\Tariff_Reference_Document_13_March_2019.pdf"

embeddings = RiskAzureOpenAIEmbeddings(openai_api_key=api_key)
llm = RiskAzureChatOpenAI(openai_api_key=api_key, temperature=0.)

# Implementation using streamlit
def load_chunk_persist_pdf() -> Chroma:
    pdf_folder_path = "Files"
    documents = []
    for file in os.listdir(pdf_folder_path):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, "Tariff_Reference_Document_13_March_2019_New.pdf")
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_documents = text_splitter.split_documents(documents)
    
    vectordb = Chroma.from_documents(
        documents=chunked_documents,
        embedding=embeddings,
        persist_directory="db/all_refined/Tariff"
    )
    vectordb.persist()
    return vectordb

def create_agent_chain():
    chain = load_qa_chain(llm, chain_type="stuff", verbose=True)
    return chain

def get_llm_response(query):
    vectordb = load_chunk_persist_pdf()
    chain = create_agent_chain()
    matching_docs = vectordb.similarity_search(query)
    answer = chain.run(input_documents=matching_docs, question=query)
    return answer


# Streamlit UI
# ===============
st.set_page_config(page_title="Doc Searcher", page_icon=":robot:")
st.header("Query PDF Source")

form_input = st.text_input('Enter Query')
submit = st.button("Generate")

if submit:
    st.write(get_llm_response(form_input))