from langchain.chat_models import init_chat_model
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
load_dotenv(override = True)


def talk_with_gpt(model_name: str,prompt: str, messages: list | None = []) -> str:
    messages.append(HumanMessage(content = prompt))
    print(messages)
    model = init_chat_model(model = model_name)
    response = model.invoke(messages)
    messages.append(AIMessage(response.text))
    print(messages)
    return response.text