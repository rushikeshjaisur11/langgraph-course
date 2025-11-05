from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel,Field
from langchain_openai import ChatOpenAI
from dotenv import find_dotenv,load_dotenv


class RouterQuery(BaseModel):
    """ Route a query to most relevent data source """
    
    datasource: Literal["vectorstore","websearch"] = Field(
        description="Given a user question choose to route it to web search or a vectorstore."
        )
    
llm = ChatOpenAI(temperature=0)
strucured_llm_router  =  llm.with_structured_output(RouterQuery)

system = """
You are expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
use the vectorstore for the questions on theses topics. For all other use web-search.
"""

router_prompt = ChatPromptTemplate.from_messages([
    ("system",system),
    ("human","{question}")
])
question_router = router_prompt | strucured_llm_router