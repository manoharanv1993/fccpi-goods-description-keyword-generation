from client import RiskAzureChatOpenAI 
from client import RiskAzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_community.document_loaders import PyPDFLoader
import json
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
load_dotenv()

api_key = ""
DOC_PATH = "document.json"

embeddings = RiskAzureOpenAIEmbeddings(openai_api_key=api_key)
llm = RiskAzureChatOpenAI(openai_api_key=api_key, temperature=0.)
description=""
test_llm_result = llm.invoke("Generate a keyword most suitable for this description - Protective and decontamination goods, specially designed or modified for military use, components and chemical mixtures as follows")
print(test_llm_result)
