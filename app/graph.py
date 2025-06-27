from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from typing import  Annotated   
from typing_extensions import TypedDict
llm= init_chat_model(model_provider="openai", model="gpt-4o-mini")
class State(TypedDict):
    messages:Annotated[list,add_messages]
graph_builder = StateGraph(State)

def chat(state:State):
    return { "messages": [llm.invoke(state["messages"])] }
graph_builder.add_node("chatbot", chat)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph=graph_builder.compile()
def create_graph_checkpoint(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)   