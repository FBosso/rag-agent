from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from nodes import agent
from state_schema import AgentState
from tools import all_tools

graph = StateGraph(AgentState)

graph.add_node("agent",agent)
graph.add_edge(START, "agent")

tools = ToolNode(all_tools)
graph.add_node("tools", tools)

graph.add_conditional_edges(
    "agent",
    tools_condition,
)
graph.add_edge("tools", "agent")

memory = MemorySaver()
app = graph.compile()
