from graph.chains.generation import generation_chain
from graph.state import GraphState


def generate(state: GraphState):
    question = state["question"]
    docuements = state["documents"]
    
    generation = generation_chain.invoke({"context":docuements,"question":question})
    
    return {"documents":docuements,"question":question,"generation":generation}