from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState,END,StateGraph
from dotenv import load_dotenv,find_dotenv
from nodes import run_agent_reasoning,tool_node

load_dotenv(find_dotenv())

AGENT_REASON = "agent_reason"
ACT = "act"
LAST = -1 

def should_continue(state:MessagesState):
    if  not state["messages"][LAST].tool_calls:
        return END
    return ACT

flow = StateGraph(state_schema=MessagesState)
flow.add_node(AGENT_REASON,run_agent_reasoning)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT,tool_node)
flow.add_conditional_edges(AGENT_REASON,should_continue,{END:END,ACT:ACT})
flow.add_edge(ACT,AGENT_REASON)


graph = flow.compile()

print(graph.get_graph().draw_mermaid())

if __name__ == "__main__":
    res = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What is the weather in Pune, India ? List it in fahrenheit  and Celcius and triple them"
                )
            ]
        }
    )
    print(res['messages'][LAST].content)