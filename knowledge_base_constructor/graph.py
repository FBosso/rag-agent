from langgraph.graph import END, START, StateGraph

from knowledge_base_constructor.nodes import articles_node, interviews_node, store_node, video_node
from knowledge_base_constructor.state_schema import ConstructorState

graph = StateGraph(ConstructorState)

graph.add_node("articles", articles_node)
graph.add_node("interviews", interviews_node)
graph.add_node("video", video_node)
graph.add_node("store_knowledge", store_node)

# fan-out: the three source agents run in parallel branches from START
graph.add_edge(START, "articles")
graph.add_edge(START, "interviews")
graph.add_edge(START, "video")

# fan-in: store_knowledge only runs once all three branches have completed
graph.add_edge("articles", "store_knowledge")
graph.add_edge("interviews", "store_knowledge")
graph.add_edge("video", "store_knowledge")
graph.add_edge("store_knowledge", END)

app = graph.compile()
