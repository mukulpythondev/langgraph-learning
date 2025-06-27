from typing import Annotated
from pydantic import BaseModel
from typing_extensions import TypedDict
from langsmith.wrappers import wrap_openai
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

from langgraph.graph import StateGraph, START, END
class State(TypedDict):
    user_message: str
    is_coding_question: bool
    ai_message:str

class DetectCallResponse(BaseModel):
    is_coding_question: bool
class CodingAIResponse(BaseModel):
    answer: str
graph_builder = StateGraph(State)
client= wrap_openai(OpenAI())

# llm = init_chat_model("openai:gpt-4.1")
def detect_query(state:State):
    message= state.get("user_message")
    # llm call
    SYSTEM_PROMPT=""" You are a helpful assistant that detects if a user query is a coding question or not.
    return the response in the specified json format only."""
    result = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=DetectCallResponse,
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": message }
        ]
    )
    # print(result)
    state["is_coding_question"] = result.choices[0].message.parsed.is_coding_question
    return state
def route_edge(state:State):    
    if state.get("is_coding_question"):
        return "solve_coding_query"
    else:
        return "solve_query"
def solve_coding_query(state:State):
    message = state.get("user_message")
    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to resolve the user query based on coding 
    problem he is facing
    """

    result = client.beta.chat.completions.parse(
        model="gpt-4.1",
        response_format=CodingAIResponse,
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": message }
        ]
    )
    state["ai_message"] = result.choices[0].message.parsed.answer
    return state
def solve_query(state:State):
    message = state.get("user_message")
    SYSTEM_PROMPT = """
    You are an AI assistant. Your job is to chat with user
    """
    result = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=CodingAIResponse,
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": message }
        ]
    )
    state["ai_message"] = result.choices[0].message.parsed.answer
    return state
    # state["ai_message"] =  message
    
graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("solve_coding_query", solve_coding_query)
graph_builder.add_node("solve_query", solve_query)
graph_builder.add_node("route_edge", route_edge)
graph_builder.add_edge(START, "detect_query")
graph_builder.add_conditional_edges("detect_query",route_edge)
graph_builder.add_edge("solve_coding_query", END)
graph_builder.add_edge("solve_query", END)
graph = graph_builder.compile()

def call_graph():
    state = {
        "user_message": "why Google is better than Openai!",
        "ai_message": "",
        "is_coding_question": False
    }
    
    result = graph.invoke(state)
    

    print("Final Result", result)

call_graph()