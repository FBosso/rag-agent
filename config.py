import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
PDF_DIR = PROJECT_ROOT / "documents"
VECTORS_DIR = PROJECT_ROOT / "vectors"

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Add it to your environment or .env file.")

# single initialization of the models and embedder
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

# local vector database
vector_store = Chroma(persist_directory=str(VECTORS_DIR), embedding_function=embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
