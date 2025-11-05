from dotenv import find_dotenv,load_dotenv
from langgraph.graph import END,StateGraph
from graph.chains.answer_grader import answer_grader
from graph.chains.hallucination_grader import hallucination_grader_chain
from graph.consts import RETRIEVE,GENERATE,GRADE_DOCUMENTS,WEBSEARCH
from graph.nodes import generate,grade_documents,retrieve,web_search
from graph.state import GraphState
from graph.chains.router import RouterQuery, question_router
load_dotenv(find_dotenv())


def decide_to_generate(state:GraphState):
    if state["web_search"]:
        return WEBSEARCH
    return GENERATE
def route_question(state: GraphState):
    question = state["question"]
    source:RouterQuery = question_router.invoke({"question":question})
    
    if source.datasource == "websearch":
        return WEBSEARCH
    elif source.datasource == "vectorstore":
        return RETRIEVE
    
def grade_generation(state: GraphState):
    question = state["question"]
    documents = state["documents"]
    generation = state['generation']
    
    score = hallucination_grader_chain.invoke({"documents":documents,"generation":generation})
    
    if hallucinatiion_score := score.binary_score:
        
        score = answer_grader.invoke({"question":question,"generation":generation})
        if answer_grade := score.binary_score:
            return "useful"
        else:
            return "not useful"
    else:
        return "not supported"

workflow = StateGraph(state_schema=GraphState)
workflow.add_node(RETRIEVE,retrieve)
workflow.add_node(GRADE_DOCUMENTS,grade_documents)
workflow.add_node(WEBSEARCH,web_search)
workflow.add_node(GENERATE,generate)

# workflow.set_entry_point(RETRIEVE)
workflow.set_conditional_entry_point(
    route_question, {WEBSEARCH: WEBSEARCH, RETRIEVE: RETRIEVE}
)
workflow.add_edge(RETRIEVE,GRADE_DOCUMENTS)
workflow.add_conditional_edges(GRADE_DOCUMENTS,decide_to_generate,{WEBSEARCH:WEBSEARCH,GENERATE:GENERATE})
workflow.add_conditional_edges(GENERATE,grade_generation, {"useful":END,"not useful":WEBSEARCH,"not suported":GENERATE})
workflow.add_edge(WEBSEARCH,GENERATE)
workflow.add_edge(GENERATE,END)
 
graph = workflow.compile()
