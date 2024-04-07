import time
import json
import os
import subprocess

from jinja2 import Environment, BaseLoader

from agents.patcher import Patcher

from llm import LLM

PROMPT = open("agents/runner/prompt.jinja2", "r").read().strip()

class Runner:
    def __init__(self, base_model: str):
        self.base_model = base_model
        self.llm = LLM(model_id=base_model)

    def render(self, request) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(request=request)


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
        
    def validate_rerunner_response(self, response: str):
        response = response.strip().replace("```json", "```")
        
        if response.startswith("```") and response.endswith("```"):
            response = response[3:-3].strip()
 
        print(response)
 
        try:
            response = json.loads(response)
        except Exception as _:
            return False
        
        print(response)

        if "action" not in response and "response" not in response:
            return False
        else:
            return response

    def run_code(
        self,
        commands: list,
        project_path: str,
    ):  
        
        for command in commands:
            command_set = command.split(" ")
            
            process = subprocess.run(
                command_set,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=project_path
            )
            command_output = process.stdout.decode('utf-8')
            command_failed = process.returncode != 0
            return 

    def execute(self, request):
        prompt = self.render(request)
        response = self.llm.inference(prompt)
        
        valid_response = self.validate_response(response)
        
        print("=====" * 10)
        print(valid_response)
        
        self.run_code(valid_response)

        return valid_response