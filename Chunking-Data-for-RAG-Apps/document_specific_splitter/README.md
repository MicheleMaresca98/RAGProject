# Document Specific Splitter - Python Demo

This demo shows how to create chunks of a Python code sample using Langchain's `RecursiveCharacterTextSplitter` method and add them to a new collection in an MongoDB Atlas Cluster with vector embeddings. 

## Prerequisites

- Atlas Cluster Connection String
- Open AI API Key

## Setup

Install the requirements:

```bash
pip3 install -r requirements.txt
```

Add your Connection String and LLM API Key to the `.env` file.


## Usage

Run the demo:

```bash
python3 python_splitter.py
```