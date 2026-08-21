# RAG Agent

A small chat agent that answers questions using your own documents. Drop some PDFs in, ask questions in the terminal, and it looks things up instead of just guessing.

## How it works

Under the hood it's a simple retrieval-augmented generation setup: your PDFs get split into chunks and embedded into a local vector store, and when you ask something, the agent searches that store for relevant context before answering.

## Getting started

1. Install dependencies:
   ```
   uv sync
   ```

2. Add your OpenAI API key to a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your-key-here
   ```

3. Drop some PDFs into the `documents/` folder, then ingest them:
   ```
   python ingest_documents.py
   ```

4. Start chatting:
   ```
   python main.py
   ```

   Type your questions, and type `exit` whenever you're done.

## Project layout

- `config.py` – model, embedder, and vector store setup
- `ingest_documents.py` – loads PDFs and stores them as vectors
- `main.py` – the chat loop
- `graph.py`, `nodes.py`, `tools.py`, `state_schema.py` – the agent's internal wiring
- `documents/` – where you put source PDFs
- `vectors/` – the local vector database