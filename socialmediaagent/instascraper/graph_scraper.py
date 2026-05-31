import os
from functools import cache
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt.tool_node import ToolNode
from langgraph.graph import StateGraph, START, END
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from tools_scraper import InstagramScraper
from prompts_scraper import SYSTEM_SCRAPER_PROMPT, SYSTEM_SUMMARIZATION_MESSAGE
from schemas_scraper import InstagramState

from dotenv import load_dotenv
load_dotenv()

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


@cache
def get_credentials() -> InstagramScraper:
    return InstagramScraper(username = INSTAGRAM_USERNAME, password = INSTAGRAM_PASSWORD)

@cache
def get_scraper_agent():
    creds = get_credentials()
    agent = create_agent(
            model = "gpt-4o-mini",
            tools = [creds.get_user_info, creds.get_user_medias]
        )

    return agent

@cache
def get_summarization_agent():
    agent = create_agent(
        model = "gpt-5.4-mini"
    )

    return agent

def should_continue(state: InstagramState):
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return "llm_summarize_call"
    
    tool_names = {tc["name"] for tc in last_message.tool_calls}
    
    if "get_user_info" in tool_names:
        return "bio_scraper"
    elif "get_user_medias" in tool_names:
        return "post_scraper"
    
    return "llm_summarize_call"

def call_scraper_llm(state: InstagramState):
    try:
        instagram_agent = get_scraper_agent()
        response = instagram_agent.invoke({"messages": [
            {
                "role": "system",
                "content": SYSTEM_SCRAPER_PROMPT
            },
            {
                "role": "user",
                "content": state["messages"]
            }
            ]
        })
        
        return {"messages": [response["messages"][-1]]}
    
    except Exception as e:
        print(f"LLM i çağırırken hata alındı: {e}")
        return {"messages": [AIMessage(content=f"Hata: {e}")]}

def call_summarizer_llm(state: InstagramState):
    try:
        instagram_agent = get_summarization_agent()
        response = instagram_agent.invoke({"messages": [
            {
                "role": "system",
                "content": SYSTEM_SUMMARIZATION_MESSAGE
            },
            {
                "role": "user",
                "content": state["messages"]
            }
            ]
        })

        return {"messages": [response["messages"][-1]]}
    
    except Exception as e:
        print(f"LLM i çağırırken hata alındı: {e}")
        return {f"messages": [AIMessage(content=f"Hata: {e}")]}

def build_graph_for_scrape():
    try:
        creds = get_credentials()
        memory = MemorySaver()

        graph_builder = StateGraph(InstagramState)

        graph_builder.add_node("post_scraper", ToolNode([creds.get_user_medias]))
        graph_builder.add_node("bio_scraper", ToolNode([creds.get_user_info]))
        graph_builder.add_node("llm_scraper_call",call_scraper_llm)
        graph_builder.add_node("llm_summarize_call", call_summarizer_llm)

        graph_builder.add_edge(START, "llm_scraper_call")
        graph_builder.add_conditional_edges(
            "llm_scraper_call",
            should_continue, 
            {
                "bio_scraper": "bio_scraper", 
                "post_scraper": "post_scraper",
                "llm_summarize_call": "llm_summarize_call"
            }
        )
        graph_builder.add_edge("bio_scraper", "llm_scraper_call")
        graph_builder.add_edge("post_scraper", "llm_scraper_call")
        graph_builder.add_edge("llm_summarize_call", END)

        graph = graph_builder.compile(checkpointer = memory)

        return graph

    except Exception as e:
        print(f"Graph build edilirken bir hata oldu: {e}")

def chat_with_ai(graph, prompt:str):
    config = {"configurable":{"thread_id":"123"}}
    response = graph.invoke({"messages": [HumanMessage(prompt)]}, config = config)
    return response["messages"][-1]