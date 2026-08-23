from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from config import llm
from knowledge_base_constructor.search_tools import article_tools, interview_tools, video_tools
from knowledge_base_constructor.state_schema import SourceAgentState

MAX_SEARCHES_INSTRUCTION = (
    " Run at most 3 distinct searches to gather material, then stop calling tools "
    "and reply with a short confirmation instead."
)

ARTICLES_SYSTEM_PROMPT = (
    "You are a research assistant gathering background articles and news about a public person."
    + MAX_SEARCHES_INSTRUCTION
)
INTERVIEWS_SYSTEM_PROMPT = (
    "You are a research assistant gathering written interviews about a public person."
    + MAX_SEARCHES_INSTRUCTION
)
VIDEO_SYSTEM_PROMPT = (
    "You are a research assistant gathering video interview transcripts about a public person. "
    "First search YouTube, then fetch the transcript of the most relevant videos."
    + MAX_SEARCHES_INSTRUCTION
)


def _build_source_agent(tools: list):
    llm_with_tools = llm.bind_tools(tools)

    def agent(state: SourceAgentState) -> SourceAgentState:
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    graph = StateGraph(SourceAgentState)
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    return graph.compile()


articles_app = _build_source_agent(article_tools)
interviews_app = _build_source_agent(interview_tools)
video_app = _build_source_agent(video_tools)
