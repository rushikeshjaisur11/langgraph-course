from typing import Any, Dict

from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState


def grade_documents(state: GraphState)->Dict[str,Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set flag to run web search
    

    Args:
        state (GraphState): The current state of the graph

    Returns:
        Dict[str,Any]: Filtered out irrelevant docuemnts and updated web search flag
    """
    question = state["question"]
    documents = state["documents"]
    
    filtered_docs = []
    web_search = False
    for d in documents:
        score = retrieval_grader.invoke({"question":question,"document":d.page_content})
        grade = score.binary_score
        if grade.lower()=='yes':
            filtered_docs.append(d)
        else:
            web_search=True
    return {"documents":filtered_docs,"question":question,"web_search":web_search}
        