from graph import create_graph_checkpoint
from dotenv import load_dotenv
import json
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.types import Command
load_dotenv()
MONGODB_URI = "mongodb://admin:admin@localhost:27017"
config = {"configurable": {"thread_id": "1"}}
 
def init():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_graph_checkpoint(checkpointer=checkpointer)
    
        state =graph_with_mongo.get_state(config=config)
        # print(state)
        # for message in state.values['messages']:
        #     message.pretty_print()
        last_message= state.values['messages'][-1]
        # print(last_message)
        tool_calls=last_message.additional_kwargs.get("tool_calls",[])
        for call in tool_calls:
            if call.get("function" , {}).get("name")== "human_assistance_tool":
                args= call.get("function", {}).get("arguments", "{}")
                try:
                    args_dict=json.loads(args)
                    user_query= args_dict.get("query")
                except json.JSONDecodeError:
                    print("Failed to decode JSON from tool call arguments.")
        print("User is trying to ask",user_query)
        ans=input("Resolve the query")
        resume_command= Command(resume={"data":ans})
        for event in graph_with_mongo.stream(resume_command, config=config, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()



init()