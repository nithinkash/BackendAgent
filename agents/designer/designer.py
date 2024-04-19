from llm import LLM
import json 
from jinja2 import Environment, BaseLoader
import subprocess
import os 

from logger import Logger

logger =Logger("designer.log")

PROMPT = open("agents/designer/prompt.jinja2", "r").read().strip()

class Designer:
    def __init__(self, base_model) -> None:
        self.llm = LLM(model_id=base_model)
        logger.info("Loading previous conversations and backend Design schema")
        with open(os.path.join(os.getcwd(),".assets/designChat.json"), "r+") as json_file:
            self.conversations = json.load(json_file)
        json_file.close()

    def render(self):
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(conversations=self.conversations)
    
    def validate_response(self, response: str):
        response = response.strip().replace("```json", "```")
        
        if response.startswith("```") and response.endswith("```"):
            response = response[3:-3].strip()
 
        try:
            response = json.loads(response)
        except Exception as _:
            return False

        if "commands" not in response:
            return False
        else:
            return response["commands"]
        
    def run_code(self, commands, project_path=os.path.join(os.getcwd(), "db")):  
    
        command_set = "sqlite3 BackendAgent.db '{}'".format("; ".join(commands[1:]))
            
        process = subprocess.Popen(
            command_set,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=project_path,
            shell=True
            )
      
        output, error = process.communicate()
        if output:
            logger.info(output)
        else:
            logger.error(error)
        return 
    
    def execute(self):
        prompt = self.render()
        logger.info(prompt)
        response = self.llm.inference(prompt)
        logger.info("LLM Responded with: "+ response)

        valid_response = self.validate_response(response)
        
        print("=====" * 10)
        print(valid_response)
        
        if valid_response:
            self.run_code(valid_response)
            logger.info("Design has been succesully loaded to LLM: {}".format(response))


            self.conversations["messages"].append({
                "role": "User",
                "content": prompt
            })

            self.conversations["messages"].append({
                "role": "BackendAgent",
                "content": response
            })
            with open(os.path.join(os.getcwd(),".assets/designChat.json"), "r+") as json_file:
                json.dump(self.conversations, json_file, indent=4)
        else:
            logger.error("Something wrong with the response from LLM")

        return 

    