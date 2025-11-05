from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import find_dotenv,load_dotenv
load_dotenv(find_dotenv())
class GradeAnswer(BaseModel):
    
    binary_score:bool = Field(description="Answer the question 'yes' or 'no' ")
    
    
llm = ChatOpenAI(name ="answer_grader",model='gpt-4-turbo',temperature=0)
strucurted_answer_llm_grader = llm.with_structured_output(GradeAnswer)

system = """
You are a grader assessing whether an answer addresses / resolved a question
Give binary score 'yes' or 'no'. 'Yes' means that answer resolved the question.
"""

answer_prompt_template = ChatPromptTemplate.from_messages([
    ("system",system),
    ("human","User question : {question} \n LLM Generateion {generation}")
])

answer_grader = answer_prompt_template | strucurted_answer_llm_grader