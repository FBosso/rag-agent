import operator
from collections.abc import Sequence
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class SourceAgentState(TypedDict):
    """State for a single search sub-agent (articles/interviews/video)."""
    messages: Annotated[Sequence[BaseMessage], add_messages]


class ConstructorState(TypedDict):
    name: str
    surname: str
    description: str
    person_id: str
    collected_documents: Annotated[list[dict], operator.add]
