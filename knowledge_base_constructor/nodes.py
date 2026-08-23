from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import get_vector_store
from knowledge_base_constructor.state_schema import ConstructorState
from knowledge_base_constructor.sub_agents import (
    ARTICLES_SYSTEM_PROMPT,
    INTERVIEWS_SYSTEM_PROMPT,
    VIDEO_SYSTEM_PROMPT,
    articles_app,
    interviews_app,
    video_app,
)


def _person_query(state: ConstructorState) -> str:
    query = f"{state['name']} {state['surname']}"
    if state.get("description"):
        query += f" ({state['description']})"
    return query


def _run_source_agent(app, system_prompt: str, state: ConstructorState, source_type: str) -> dict:
    result = app.invoke(
        {
            "messages": [
                SystemMessage(system_prompt),
                HumanMessage(f"Research: {_person_query(state)}"),
            ]
        }
    )
    documents = [
        {
            "content": message.content,
            "metadata": {
                "person_id": state["person_id"],
                "name": state["name"],
                "surname": state["surname"],
                "source_type": source_type,
            },
        }
        for message in result["messages"]
        if isinstance(message, ToolMessage) and message.content
    ]
    return {"collected_documents": documents}


def articles_node(state: ConstructorState) -> dict:
    """Runs the articles/news search sub-agent."""
    return _run_source_agent(articles_app, ARTICLES_SYSTEM_PROMPT, state, "article")


def interviews_node(state: ConstructorState) -> dict:
    """Runs the written-interviews search sub-agent."""
    return _run_source_agent(interviews_app, INTERVIEWS_SYSTEM_PROMPT, state, "interview")


def video_node(state: ConstructorState) -> dict:
    """Runs the video-interview search sub-agent."""
    return _run_source_agent(video_app, VIDEO_SYSTEM_PROMPT, state, "video")


def store_node(state: ConstructorState) -> dict:
    """Chunks and embeds everything gathered by the search sub-agents into the person's collection."""
    documents = [
        Document(page_content=doc["content"], metadata=doc["metadata"])
        for doc in state["collected_documents"]
    ]
    if not documents:
        print(f"No content gathered for {state['name']} {state['surname']}.")
        return {}

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    vector_store = get_vector_store(state["person_id"])
    vector_store.add_documents(chunks)
    print(
        f"Stored {len(chunks)} chunks for {state['name']} {state['surname']} "
        f"in collection '{state['person_id']}'."
    )
    return {}
