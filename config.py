import os
import re
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


def get_vector_store(collection_name: str | None = None) -> Chroma:
    """Returns a Chroma vector store, optionally scoped to a specific collection.

    Args:
        collection_name (str | None): name of the collection (e.g. a person's slug).
            Omit to use the default collection.

    Returns:
        Chroma: the vector store, sharing the same on-disk persist directory as `vector_store`
    """
    kwargs = {"persist_directory": str(VECTORS_DIR), "embedding_function": embeddings}
    if collection_name:
        kwargs["collection_name"] = collection_name
    return Chroma(**kwargs)


def slugify_person(name: str, surname: str) -> str:
    """Builds a stable collection identifier from a person's name and surname."""
    raw = f"{name}-{surname}".strip().lower()
    return re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
