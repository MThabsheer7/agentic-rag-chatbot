from utils import get_doc_tools
from llama_index.core.settings import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex

class MultiDocAgent:
    def __init__(self, config):
        self.doc_to_tools_dict = {}
        Settings.llm = OpenAI(model="gpt-4o", api_key=config['api']['openai'])

    def process_documents(self, doc_name_mapping):
        for docname, docpath in doc_name_mapping.items():
            vec_tool, summ_tool = get_doc_tools(docpath, docname)
            self.doc_to_tools_dict[docname] = [vec_tool, summ_tool]
        