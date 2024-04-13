from llm import LLM
import json 
from jinja2 import Environment, BaseLoader
import subprocess

from logger import Logger

logger =Logger()

PROMPT = open("agents/designer/prompt.jinja2", "r").read().strip()

class Designer:
    def __init__(self, base_model) -> None:
        self.llm = LLM(model_id=base_model)
        logger.info("Loading previous conversations and backend Design schema")
        with open("/Users/nithinkashyap/MyProjects/BackendAgent/.assets/designChat.json", "r") as json_file:
            self.conversations = json.load(json_file)

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
        
    def run_code(self, commands, project_path="/Users/nithinkashyap/MyProjects/BackendAgent/db"):  
        
        for command in commands:
            command_set = command.split(" ")
            
            process = subprocess.run(
                command_set,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=project_path
            )
            command_output = process.stdout.decode('utf-8')
            logger.info(command_output)
            command_failed = process.returncode != 0
            if command_failed:
                logger.error(command_failed)
            return 
    
    def execute(self):
        prompt = self.render()
        print(prompt)
        response = self.llm.inference(prompt)
        print(response)
        
        valid_response = self.validate_response(response)
        
        print("=====" * 10)
        print(valid_response)
        
        if valid_response:
            self.run_code(valid_response)
            logger.info("Design has been succesully loaded to LLM: ", response)
        else:
            logger.error("Something wrong with the response from LLM")

    