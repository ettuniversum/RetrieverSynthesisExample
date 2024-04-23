# pip install llama-index
# pip install llama-index-llms-ollama
# pip install llama-index-retrievers-bm25
from os import getcwd
from llama_index.core import SimpleDirectoryReader, PromptTemplate, get_response_synthesizer
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.ollama import Ollama
from llama_index.retrievers.bm25 import BM25Retriever
import time


llm = Ollama(model="codellama", request_timeout=60.0, temperature=0)

qa_prompt_tmpl = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query.\n"
    "Please reference functions, if-statements, or lines of code if possible.\n"
    "Please give minimal mitigation examples.\n"
    "Query: {query_str}\n"
    "Answer: "
)

def example_retriever_synthesis():
    current_dir = getcwd()
    file = 'conicsec.cpp'
    #file = 'line.cpp'
    file_name = current_dir+'\\'+ file
    reader = SimpleDirectoryReader(input_files=[file_name])
    documents = reader.load_data(num_workers=4)
    splitter = SentenceSplitter(chunk_size=512)
    nodes = splitter.get_nodes_from_documents(documents)
    retriever = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=2)

    #line_of_code = 'while (i != last) {'
    line_of_code = 'double b = 0.5*xC0.c[1]/xC0.c[0];'

    nodes = retriever.retrieve(file_name + ' ' + line_of_code)
    print(nodes[0].text)
    print("\n---------------------\n")
    print(nodes[1].text)

    qa_template = PromptTemplate(qa_prompt_tmpl)

    response_synthesizer = get_response_synthesizer(llm=llm, text_qa_template=qa_template, response_mode="compact")

    #report_msg = 'changing xs on every loop'
    report_msg = 'shadowed local variable'
    query_str = f"How is {report_msg} a vulnerability with this line of code {line_of_code}?"

    start_time = time.time()
    response = response_synthesizer.get_response(
        query_str=query_str, text_chunks=[nodes[0].text,  nodes[1].text],
    )
    stop_time = time.time()
    print(f"Seconds: "+ str(stop_time-start_time))
    print(response)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    example_retriever_synthesis()

