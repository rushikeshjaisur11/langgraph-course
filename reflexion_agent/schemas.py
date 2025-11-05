from pydantic import BaseModel,Field


class Reflection(BaseModel):
    """ Reflection on the answer"""
    missing:str = Field(description='Critique of what is missing')
    superfluous: str = Field(description="Critique of what is superfluous") 
    

class AnswerQuestion(BaseModel):
    """Answer the question """
    
    answer: str = Field(description="~250 word detailed answer to the question")
    reflection: Reflection = Field(description="description on the initial answer")
    search_queries: list[str] = Field(description="1-3 search queries for researching improvements to address the critique of your answer.")
    

class ReviseAnswer(AnswerQuestion):
    """Revised answer"""
    
    reference: list[str] = Field(description="Citations motivating your updated answer.")