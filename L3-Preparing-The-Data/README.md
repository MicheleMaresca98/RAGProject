# Code Summary: Preparing the Data for our RAG System

Below is an overview of the code that sanitizes the data, chunks it, generates metadata, creates embeddings, and stores it in MongoDB. You can also view and fork the code from the Curriculum GitHub repository.

## Prerequisites

* Atlas Cluster Connecting String
* OpenAI API Key


## Usage

Install the requirements:
```
pip3 install langchain langchain_community langchain_core langchain_openai langchain_mongodb pymongo pypdf
```

Create a key_param file with the following content:
```
MONGODB_URI=<your_atlas_connection_string>
LLM_API_KEY=<your_llm_api_key>
```

load_data.py file

This code ingests a pdf, removes empty pages, chunks the pages into paragraphs, generates metadata for the chunks, creates embeddings, and stores the chunks and their embeddings in a MongoDB collection.

Reference: https://github.com/mongodb-university/curriculum/tree/main/Atlas-Vector-Search