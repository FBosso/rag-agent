from config import llm
from state_schema import AgentState
from tools import all_tools

llm_with_tools = llm.bind_tools(all_tools)


def agent(state: AgentState) -> AgentState:
    """Node invoking the llm with available tools"""
    response = llm_with_tools.invoke(state['messages'])
    return {"messages":[response]}

def should_continue(state: AgentState) -> str:
    if state['messages'][-1] == 'exit':
        return 'end'
    else:
        return "continue"