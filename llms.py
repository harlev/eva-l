from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from abc import ABC, abstractmethod
from pydantic import BaseModel
import time
import os

load_dotenv()


class LLMInterface(ABC):
    @abstractmethod
    def generate(self, messages: list[BaseMessage], model: str = "gpt-4o-mini", api_key: str = None) -> str:
        pass
    
    @abstractmethod
    def generate_structured(self, messages: list[BaseMessage], pydantic_object: BaseModel, model: str = "gpt-4o-mini", api_key: str = None) -> str:
        pass

class OpenAILLM(LLMInterface):
    def generate(self, messages: list[BaseMessage], model: str = "gpt-4o-mini", api_key: str = None) -> str:
        model = ChatOpenAI(model=model, api_key=api_key)
        parser = StrOutputParser()
        chain = model | parser
        return chain.invoke(messages)
    
    def generate_structured(self, messages: list[BaseMessage], pydantic_object: BaseModel, model: str = "gpt-4o-mini", api_key: str = None) -> str:
        model = ChatOpenAI(model=model, api_key=api_key)
        structured_llm = model.with_structured_output(pydantic_object)
        return structured_llm.invoke(messages)

class MockLLM(LLMInterface):
    def generate(self, messages: list[BaseMessage], model: str = "gpt-4o-mini", api_key: str = None) -> str:
        time.sleep(2)
        return f"Mock response: {messages}"
    
    def generate_structured(self, messages: list[BaseMessage], pydantic_object: BaseModel, model: str = "gpt-4o-mini", api_key: str = None) -> str:
        fields = pydantic_object.model_fields.keys()
        return pydantic_object(**{field: f"Mock {field} content" for field in fields})

if __name__ == "__main__":
    messages = [
        SystemMessage(content="Translate the following from English into Italian"),
        HumanMessage(content="hi!"),
    ]
    llm = OpenAILLM()
    print(llm.generate(messages, api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini"))
    
    class Joke(BaseModel):
        setup: str
        punchline: str

    messages = [
        HumanMessage(content="Tell me a joke about cats"),
    ]

    print(llm.generate_structured(messages, Joke))

    llm = MockLLM()
    print(llm.generate(messages))
    print(llm.generate_structured(messages, Joke))
