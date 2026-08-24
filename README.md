# RAG Agent

A small toolkit for building and chatting with your own knowledge bases. Feed it documents (your own PDFs, or research gathered automatically from the web) and ask questions in the terminal instead of guessing.

## How it works

Under the hood it's a retrieval-augmented generation setup built on LangGraph: content gets split into chunks and embedded into a local vector store, and when you ask something, an agent searches that store for relevant context before answering. Knowledge bases can be filled in two ways: by pointing the agent at your own PDFs, or by letting a multi-agent researcher search the web, interviews, and video transcripts for a given person and store what it finds.

## Getting started

1. Install dependencies:
   ```
   uv sync
   ```

2. Add your OpenAI API key to a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your-key-here
   ```

3. Build a knowledge base, either by:
   - dropping PDFs into the `documents/` folder and ingesting them, or
   - running the knowledge base constructor to research a person from the web

4. Start chatting with the agent about the ingested content.

## Project layout

- `config.py` – shared model, embedder, and vector store setup
- `ingest_documents.py` – loads PDFs and stores them as vectors
- `main.py`, `graph.py`, `nodes.py`, `tools.py`, `state_schema.py` – the chat agent and its internal wiring
- `knowledge_base_constructor/` – multi-agent pipeline that researches a person online and stores what it finds
- `documents/` – where you put source PDFs
- `vectors/` – the local vector database
- `notebooks/` – exploratory notebooks (e.g. visualizing stored vectors)

## License

MIT — see [LICENSE](LICENSE).