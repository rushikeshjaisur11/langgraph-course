from dotenv import find_dotenv,load_dotenv
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from react import llm,tools

load_dotenv(find_dotenv())

SYSTEM_PROMPT = """
You are helpful assistant that can use tools to anwer the questions.
"""

def run_agent_reasoning(state: MessagesState):
    """ Run the agent reasoning node. """
    
    response = llm.invoke([{"role":"system","content":SYSTEM_PROMPT},*state["messages"]])
    return {"messages":[response]}

tool_node = ToolNode(tools)