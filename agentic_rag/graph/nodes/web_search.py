from typing import Any,Dict
from langchain_classic.schema import Document
from langchain_tavily import TavilySearch

from graph.state import GraphState

web_search_tool = TavilySearch(max_results = 3)


def web_search(state: GraphState)->Dict[str,Any]:
    question = state["question"]
    documents = state["documents"]
    
    tavily_results = web_search_tool.invoke({"query": question})["results"]
    join_tavily_result = '\n'.join([tavily_result['content'] for tavily_result in tavily_results])
    web_results = Document(page_content=join_tavily_result)
    if documents:
        documents.append(web_results)
    else:
        documents = [web_results]
        
    return {"question": question, "documents": documents}