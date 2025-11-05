from langchain_core.messages import ToolMessage, HumanMessage
from langgraph.graph import END, StateGraph, MessagesState

from chains import revisor, first_responder
from tool_executor import execute_tools

MAX_ITERATIONS = 2

def _to_messages(out):
    """Normalize various runnable outputs to a list of messages."""
    if isinstance(out, dict) and "messages" in out:
        return out["messages"]
    if isinstance(out, list):
        return out
    return [out]


def draft_node(state: MessagesState):
    out = first_responder.invoke({"messages": state.get("messages", [])})
    return {"messages": _to_messages(out)}


def execute_tools_node(state: MessagesState):
    out = execute_tools.invoke({"messages": state.get("messages", [])})
    return {"messages": _to_messages(out)}


def revise_node(state: MessagesState):
    out = revisor.invoke({"messages": state.get("messages", [])})
    return {"messages": _to_messages(out)}

builder = StateGraph(state_schema=MessagesState)
builder.add_node("draft", draft_node)
builder.add_node("execute_tools", execute_tools_node)
builder.add_node("revise", revise_node)
builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")


def event_loop(state: MessagesState) -> str:
    # state is a dict with a `messages` key when using StateGraph for messages
    messages = state.get("messages", [])
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in messages)
    num_iterations = count_tool_visits
    if num_iterations > MAX_ITERATIONS:
        return END
    return "execute_tools"


builder.add_conditional_edges(
    "revise", event_loop, {END: END, "execute_tools": "execute_tools"}
)
builder.set_entry_point("draft")
graph = builder.compile()

print(graph.get_graph().draw_mermaid())


res = graph.invoke({"messages": [HumanMessage(content="Write about latest and best agentic ai tools ")]})

# Compiled StateGraph returns a dict-like state. The messages are under the 'messages' key.
messages = res.get("messages", []) if isinstance(res, dict) else res
if messages:
    try:
        print(messages[-1].tool_calls[0]["args"]["answer"])
    except Exception:
        # best-effort: if tool_calls or structure differs, just print the last message
        print(messages[-1])

print(res)
