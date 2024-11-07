from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def openai_llm(messages: list[BaseMessage], model: str = "gpt-4o-mini"):
    model = ChatOpenAI(model="gpt-4o-mini")

    parser = StrOutputParser()
    chain = model | parser

    return chain.invoke(messages)



if __name__ == "__main__":
    messages = [
        SystemMessage(content="Translate the following from English into Italian"),
        HumanMessage(content="hi!"),
    ]
    print(openai_llm(messages))

