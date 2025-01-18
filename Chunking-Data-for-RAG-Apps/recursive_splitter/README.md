# Recursive Text Splitter PDF Demo

## Usage

The following code initializes a MongoDB collection and loads a PDF file, then splits the PDF content into chunks of 50 characters with no overlap using a recursive character text splitter. It then vectorizes these chunks using OpenAI embeddings. Finally, it stores the vectorized documents in a MongoDB Atlas cluster

```bash
python3 recursive_splitter.py
```


Reference: https://github.com/mongodb-university/curriculum/tree/main/Chunking-Data-for-RAG-Apps/