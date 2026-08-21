from langchain_core.tools import tool

from config import retriever


@tool
def retreiver_tool(query: str) -> str:
    """This tool searches and returns the most relevant infos from the vector database

    Args:
        query (str): the text query we want to compare our vectors on

    Returns:
        str: the original text coming from the vectors in our database
    """
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])

all_tools = [retreiver_tool]
