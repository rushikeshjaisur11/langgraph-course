from dotenv import find_dotenv,load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

load_dotenv(find_dotenv())

@tool
def triple(num:float) -> float:
    """Triples the given number

    Args:
        num (int): Input integer

    Returns:
        float: triple of a given number
    """
    return float(num) * 3

tools = [TavilySearch(max_results =1 ),triple]

llm = ChatOpenAI(temperature=0).bind_tools(tools)

