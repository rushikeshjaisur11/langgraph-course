from typing import TypedDict



class GraphState(TypedDict):
    """ 
    Represents the state of the graph
    Attributes : 
        question : question
        generation: LLM generated answer
        web_search: whether to add search 
        documents: list of docs 
    """
    
    question: str
    generation: str
    web_search: bool
    documents: list[str]