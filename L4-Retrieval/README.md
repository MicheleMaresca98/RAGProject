# Retrieval Demo

This demo shows how the retriever is used to retrieve relevant information for a given query. The retriever uses Atlas Vector Search to find the most relevant chunks of text from the indexed PDFs.

## Prerequisites

- Atlas Cluster Connection String
- OpenAI API Key

## Setup

Install the requirements:

```bash
pip3 install langchain langchain_community langchain_core langchain_openai langchain_mongodb pymongo pypdf
```

Create a `key_param` file with the following content:

```python
MONGODB_URI=<your_atlas_connection_string>
LLM_API_KEY=<your_llm_api_key>
```

**Note:** Replace the `MONGODB_URI` and `LLM_API_KEY` values with your own values.

Load the sample data into your Atlas Cluster (see [Preparing The Data Demo](../L3-Preparing-The-Data/README.md)):

```bash
python load_data.py
```

Create the following vector search index on the `chunked_data` collection in your Atlas Cluster:

```bash
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    },
    {
      "path": "hasCode",
      "type": "filter"
    }
  ]
}
```

**Note:** Name the index `vector_index`.

## Usage

Update the `query_data` function in the `rag.py` file by passing in a question:

```python
query_data("What is the difference between a database and collection in MongoDB?")
```

Run the demo:

```bash
python rag.py
```

Add a prefilter to the retriever by updating the `query_data` function in the `rag.py` file:

```python
def query_data(query):
    retriever = vectorStore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 3,
            "pre_filter": { "hasCode": { "$eq": False } },
            "score_threshold": 0.01
        },
    )

    results = retriever.invoke(query)
    print(results)
```