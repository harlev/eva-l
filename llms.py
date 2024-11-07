from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from abc import ABC, abstractmethod
from pydantic import BaseModel

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
    
    def generate_structured(self, messages: list[BaseMessage], pydantic_object: BaseModel, model: str = "gpt-4o-mini") -> str:
        model = ChatOpenAI(model=model)
        structured_llm = model.with_structured_output(pydantic_object)
        return structured_llm.invoke(messages)

class MockLLM(LLMInterface):
    def generate(self, messages: list[BaseMessage], model: str = "gpt-4o-mini") -> str:
        return "Mock response"
    
    def generate_structured(self, messages: list[BaseMessage], pydantic_object: BaseModel, model: str = "gpt-4o-mini") -> str:
        fields = pydantic_object.model_fields.keys()
        return pydantic_object(**{field: f"Mock {field} content" for field in fields})

if __name__ == "__main__":
    messages = [
        SystemMessage(content="Translate the following from English into Italian"),
        HumanMessage(content="hi!"),
    ]
    llm = OpenAILLM()
    print(llm.generate(messages))
    
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
