from utils import read_config
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from llama_index.core.indices import SummaryIndex, VectorStoreIndex
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from llama_index.core.tools import FunctionTool, QueryEngineTool
from typing import Optional, List
from loguru import logger

config = read_config()
openai.api_key = config['api']['openai']

class MultiDocAgent:
    def __init__(self):
        self.doc_to_tools_dict = {}
        self.llm = OpenAI(model="gpt-4o", api_key=config['api']['openai'])

    def get_doc_tools(self, file_path: str, name: str) -> str:
        """Get vector query and summary query tools from a document."""
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        splitter = SentenceSplitter(chunk_size=1024)
        nodes = splitter.get_nodes_from_documents(documents)
        vector_index = VectorStoreIndex(nodes)

        def vector_query(query: str, page_numbers: Optional[List[str]] = None) -> str:
            """Use to answer questions over the MetaGPT paper.
        
            Useful if you have specific questions over the MetaGPT paper.
            Always leave page_numbers as None UNLESS there is a specific page you want to search for.
        
            Args:
                query (str): the string query to be embedded.
                page_numbers (Optional[List[str]]): Filter by set of pages. Leave as NONE 
                    if we want to perform a vector search
                    over all pages. Otherwise, filter by the set of specified pages.
            
            """
            page_numbers = page_numbers or []
            metadata_dicts = [
                {"key": "page_label", "value": p} for p in page_numbers
            ]

            query_engine = vector_index.as_query_engine(
                similarity_top_k=2,
                filters=MetadataFilters.from_dicts(
                    metadata_dicts,
                    condition=FilterCondition.OR
                )
            )

            response = query_engine.query(query)
            return response
        
        vector_query_tool = FunctionTool.from_defaults(
            name=f"vector_tool_{name}",
            fn=vector_query
        )

        summary_index = SummaryIndex(nodes)
        summary_query_engine = summary_index.as_query_engine(
            response_mode="tree_summarize",
            use_async=True
        )
        summary_tool = QueryEngineTool.from_defaults(
            name=f"summary_tool_{name}",
            query_engine=summary_query_engine,
            description=(
                f"Useful for summarization questions related to {name}"
            )
        )

        return vector_query_tool, summary_tool

    def process_documents(self, doc_name_mapping):
        logger.info("Processing the documents...")
        for docname, docpath in doc_name_mapping.items():
            logger.info(f"Getting the tools for {docname}")
            vec_tool, summ_tool = self.get_doc_tools(docpath, docname)
            logger.success(f"Got the tools for document {docname}")
            self.doc_to_tools_dict[docname] = [vec_tool, summ_tool]
        all_tools = [t for doc in doc_name_mapping.keys() for t in self.doc_to_tools_dict[doc]]
        obj_index = ObjectIndex.from_objects(
            all_tools,
            index_cls=VectorStoreIndex
        )
        logger.info("Indexed the document tools.")
        obj_retriever = obj_index.as_retriever(similarity_top_k=3)
        logger.info("Initialized the tool retriever.")
        agent_worker = FunctionCallingAgentWorker.from_tools(
            tool_retriever=obj_retriever,
            llm=self.llm,
            verbose=True
        )
        agent = AgentRunner(agent_worker)
        logger.info("Created the agent.")
        return agent
if __name__ == "__main__":
    ma = MultiDocAgent()
    docs = {
        "jbs": "/data/thabsheer/rough/docs/261105.pdf",
        "amazon": "/data/thabsheer/rough/docs/AMZN-Q3-2024-Earnings-Release.pdf",
        "jp_morgan": "/data/thabsheer/rough/docs/jpm-4q24.pdf",
        "rakuten": "/data/thabsheer/rough/docs/24Q2tanshin_E.pdf"
    }
    agent=ma.process_documents(docs)
    print("agent built")