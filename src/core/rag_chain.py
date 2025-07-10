from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from utils.constants import DEFAULT_LLM_MODEL, DEFAULT_CONTEXT_WINDOW, PROMPT_TEMPLATE

class RAGChain:
    def __init__(self, vector_store, llm_model_name=DEFAULT_LLM_MODEL, context_window=DEFAULT_CONTEXT_WINDOW):
        self.vector_store = vector_store
        self.llm_model_name = llm_model_name
        self.context_window = context_window
        self.llm = self.initialize_llm()
        self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        self.prompt_template = self.create_prompt_template()

    def initialize_llm(self):
        llm = ChatOllama(model=self.llm_model_name, temperature=0, num_ctx=self.context_window)
        return llm

    def create_prompt_template(self):
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        return prompt_template

    def query(self, question):
        chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
        )
        response = chain.invoke(question)
        return response