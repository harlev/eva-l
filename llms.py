from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from abc import ABC, abstractmethod

load_dotenv()

class LLMInterface(ABC):
    @abstractmethod
    def generate(self, messages: list[BaseMessage], model: str = "gpt-4o-mini") -> str:
        pass

class OpenAILLM(LLMInterface):
    def generate(self, messages: list[BaseMessage], model: str = "gpt-4o-mini") -> str:
        model = ChatOpenAI(model=model)
        parser = StrOutputParser()
        chain = model | parser
        return chain.invoke(messages)

class MockLLM(LLMInterface):
    def generate(self, messages: list[BaseMessage], model: str = "gpt-4o-mini") -> str:
        return "Mock response"

if __name__ == "__main__":
    messages = [
        SystemMessage(content="Translate the following from English into Italian"),
        HumanMessage(content="hi!"),
    ]
    llm = OpenAILLM()
    print(llm.generate(messages))
    llm = MockLLM()
    print(llm.generate(messages))
