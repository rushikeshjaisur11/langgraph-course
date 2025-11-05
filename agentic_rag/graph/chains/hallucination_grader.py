from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import find_dotenv,load_dotenv
load_dotenv(find_dotenv())
llm = ChatOpenAI(name="hallucinations_grader", model="gpt-4-turbo", temperature=0)


class Hallucinations(BaseModel):
    """ Binary score for the hallucination present in the answer""" 
    
    binary_score: bool = Field(description="Answer is grounded in the facts , 'yes' or 'no' ")
    
    
strucuted_hallucinations_llm_grader = llm.with_structured_output(Hallucinations)

system = """
You are grader assessing whether the LLM generation is grounded in / supported by a set of retrieved facts \n 
Give binary score 'yes' or 'no'. 'Yes' means answer is grounded in / supported by the set of facts.
"""

hallucination_prompt = ChatPromptTemplate.from_messages([
    ("system",system),
    ("human","Set of facts: \n\n {documents} \n\n LLM generation : {generation}")
])

hallucination_grader_chain = hallucination_prompt | strucuted_hallucinations_llm_grader 