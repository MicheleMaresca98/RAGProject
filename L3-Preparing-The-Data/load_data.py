from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_transformers.openai_functions import (
    create_metadata_tagger)
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient

import key_param


client = MongoClient(key_param.MONGODB_URI)
db_name = "book_mongodb_chunks"
collection_name = "chunked_data"
collection = client[db_name][collection_name]

mongodb_documentation_path = './sample_files/mongodb.pdf'
loader = PyPDFLoader(mongodb_documentation_path)
pages = loader.load()

# Sanitizing
cleaned_pages = []
for page in pages:
    if len(page.page_content.split(" ")) > 20:
        cleaned_pages.append(page)

# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=150
)
split_docs = text_splitter.split_documents(cleaned_pages)

# Generate metadata
schema = {
    "properties": {
        "title": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "hasCode": {"type": "boolean"}
    },
    "required": ["title", "keywords", "hasCode"]
}

llm = ChatOpenAI(
    openai_api_key=key_param.LLM_API_KEY,
    temperature=0,
    model="gpt-3.5-turbo-0613"
)
document_transformer = create_metadata_tagger(metadata_schema=schema, llm=llm)
docs = document_transformer.transform_documents(cleaned_pages)

# Generate embeddings
embeddings = OpenAIEmbeddings(openai_api_key=key_param.LLM_API_KEY) # Embedding Model
vector_store = MongoDBAtlasVectorSearch.from_documents(
    split_docs, embeddings, collection=collection)
