from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
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


def query_data(query: str) -> str:
    retriever = vector_store.as_retriever(
        search_type="similarity",
        # search_type="similarity:score_threshold",
        search_kwargs={
            "k": 3, # number of documents to return
            "pre_filter": {"hasCode": {"$eq": False}},
            # "score_threshold": 0.01
        },
    )

    template = """
        Use the following pieces of context to answer the question at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Do not answer the question if there is no given context.
        Do not answer the question if it is not related to the context.
        Do not give recommendations to anything other than MongoDB.
        Context:
        {context}
        Question: {question}
        """

    custom_rag_prompt = PromptTemplate.from_template(template)

    retrieve = {
        "context": retriever | (lambda docs: "\n\n".join([d.page_content for d in docs])),
        "question": RunnablePassthrough()
    }

    llm = ChatOpenAI(openai_api_key=key_param.LLM_API_KEY, temperature=0)

    response_parser = StrOutputParser()

    rag_chain = (
        retrieve
        | custom_rag_prompt
        | llm
        | response_parser
    )

    answer = rag_chain.invoke(query)

    return answer


if __name__ == "__main__":
    query = "When did MongoDB begin supporting multi-document transactions?"
    query_data(query)
