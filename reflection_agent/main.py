from typing import TypedDict, Annotated
from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END,StateGraph
from langgraph.graph.message import add_messages
from chains import generation_chain, reflection_chain

load_dotenv(find_dotenv())

class MessageGraph(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


REFLECT = "reflect"
GENERATE = "generate"

def generate_node(state: MessageGraph):
    return {"messages":[generation_chain.invoke({"messages":state["messages"]})]}

def reflection_node(state: MessageGraph):
    res = reflection_chain.invoke({"messages":state["messages"]})
    return {"messages":[HumanMessage(content=res.content)]}

def should_continue(state: MessageGraph):
    if len(state["messages"]) > 6:
        return "STOP"
    return REFLECT
    
graph = StateGraph(state_schema=MessageGraph)
graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflection_node)
graph.set_entry_point(GENERATE)

graph.add_conditional_edges(
    GENERATE, should_continue, {REFLECT: REFLECT, "STOP": END}
)
graph.add_edge(REFLECT, GENERATE)

graph = graph.compile()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    print("Hello Reflection Agent.")