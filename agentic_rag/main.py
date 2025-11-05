from dotenv import find_dotenv,load_dotenv
from graph.graph import graph
load_dotenv(find_dotenv())

if __name__ == "__main__":
    print("Hello Agentic RAG !!!")
    graph.get_graph().draw_mermaid_png(output_file_path='graph.png')
    res = graph.invoke(input = {"question":"what is agent memory"})
    print(res)
    