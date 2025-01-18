# Semantic Text Splitter Text File Demo

This demo shows how to create chunks of a text document using Langchain's `SemanticChunker` method and add them to a new collection in an MongoDB Atlas Cluster with vector embeddings. 

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

This demo includes a sample text file in the `sample_files` directory that is ready to use. You can optionally add your own text file to the folder.

Run the demo:

```bash
python3 semantic_splitter.py
```