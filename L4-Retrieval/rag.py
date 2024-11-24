from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient

import key_param


client = MongoClient(key_param.MONGODB_URI)
db_name = "book_mongodb_chunks"
collection_name = "chunked_data"
collection = client[db_name][collection_name]
index = "vector_index"


vector_store = MongoDBAtlasVectorSearch.from_connection_string(
    key_param.MONGODB_URI,
    db_name + "." + collection_name,
    OpenAIEmbeddings(disallowed_special=(), openai_api_key=key_param.LLM_API_KEY),
    index_name=index
)


def query_data(query: str) -> None:
    retriever = vector_store.as_retriever(
        search_type="similarity",
        # search_type="similarity:score_threshold",
        search_kwargs={
            "k": 3, # number of documents to return
            "pre_filter": {"hasCode": {"$eq": False}},
            # "score_threshold": 0.01
        },
    )
    results = retriever.invoke(query)
    print(results)


if __name__ == "__main__":
    query = "When did MongoDB begin supporting multi-document transactions?"
    query_data(query)
