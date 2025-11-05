from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel,Field
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(name="retrieval_grader", model="gpt-4-turbo", temperature=0)


class GradeDocuments(BaseModel):
    """Binary sccore for relevance check on retrieved documents"""
    
    binary_score:str = Field(description="Documents are relevant to the quesiton, 'yes' or 'no'")
    
strucuted_llm_grader = llm.with_structured_output(GradeDocuments) 

system = """ You are a grader assessing relevance of a retrieved document to a user question. 
            If document contains keyword(s) or semantic meaning related to the question, grade it as relevant
            Give a binary score yes or no to indicate whether document is relevant to the question.
        """
        
grade_prompt = ChatPromptTemplate.from_messages([
    ("system",system),
    ("human","Retrieved Documents: \n{document}\n User Question : {question}")
])

retrieval_grader = grade_prompt | strucuted_llm_grader