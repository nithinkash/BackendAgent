import json

from config import Config
from logger import Logger
from llm import LLM

config = Config()
logger = Logger()
        
data = {
    "messages": []
    }

def init_design(base_model):
    
    logger.info("Let's Design the Database System")
    llm = LLM(model_id=base_model)
    prompt=" "

    logger.info("Let's start designing your Backend System")
    while(1):
        response = llm.inference(prompt=prompt)
        print("BackednAgent: ", response)

        data["messages"].append({
            "role": "BackendAgent",
            "content": response
        })

        input_from_user = input("User: ")
        if input_from_user == "exit":
            break
        
        prompt = input_from_user
        
        data["messages"].append({
            "role": "User",
            "content": input_from_user
        })
    
    with open(".assets/designChat.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    