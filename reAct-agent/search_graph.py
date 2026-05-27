from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from search_state import State
from search_tools import tavily_search_tool
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image
from dotenv import load_dotenv
load_dotenv(override = True)

class BenimAI():
    def __init__(self):
        self.llm = ChatOpenAI(model = "gpt-4o-mini")
        self.llm = self.llm.bind_tools([tavily_search_tool])

    def llm_agent(self,state: State) -> list:
        return {"messages":[self.llm.invoke(state["messages"])]}

    def should_continue(self,state: State):
        messages_all = state["messages"]
        last_message = messages_all[-1]

        if last_message.tool_calls:
            return "search_tool"
        else:
            return END

    def AIBuilder(self):
        memory = MemorySaver()
        graph_builder = StateGraph(State)

        graph_builder.add_node("llm", self.llm_agent)
        graph_builder.add_node("search_tool", ToolNode([tavily_search_tool]))

        graph_builder.add_edge(START, "llm")
        graph_builder.add_conditional_edges("llm", 
        self.should_continue,
        {
            "search_tool": "search_tool", 
            END: END
        }
        )
        graph_builder.add_edge("search_tool", "llm")
        graph = graph_builder.compile(checkpointer = memory)

        return graph

    def chat_with_ai(self,prompt:str, graph: AIBuilder) -> str:
        config = {"configurable":{"thread_id": "123"}}
        response = graph.invoke({"messages":[HumanMessage(prompt)]},config = config)
        return response["messages"][-1]
