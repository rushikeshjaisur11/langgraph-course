from langchain_classic import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

rag_prompt = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(name="generation_chain", model="gpt-4-turbo", temperature=0)
generation_chain = rag_prompt | llm | StrOutputParser()