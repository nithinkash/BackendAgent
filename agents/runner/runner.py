import time
import json
import os
import subprocess
from flask import request
from pprint import pprint

from jinja2 import Environment, BaseLoader
from logger import Logger
from llm import LLM

PROMPT_TO_DB = open("agents/runner/prompt.jinja2", "r").read().strip()
PROMPT_TO_FRONTEND = open("agents/runner/frontend.jinja2", "r").read().strip()

logger = Logger()

class Runner:
    def __init__(self, base_model: str):
        self.base_model = base_model
        self.llm = LLM(model_id=base_model)
        with open("/Users/nithinkashyap/MyProjects/BackendAgent/.assets/designChat.json", "r+") as json_file:
            self.conversations = json.load(json_file)

    def render(self, request, PROMPT) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(request=request,conversations=self.conversations)
    
    def renderFronted(self, response, PROMPT_TO_FRONTEND) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT_TO_FRONTEND)
        return template.render(reponse_from_db=response)


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

    def run_code(self,commands, project_path="/Users/nithinkashyap/MyProjects/BackendAgent/db"):  
        
        #command_set = "sqlite3 BackendAgent.db '{}'".format("; ".join(commands[1:]))
        sql_commands = "; ".join(commands[1:])
        formatted_command = "sqlite3 BackendAgent.db <<< '{}'" #"'sqlite3 BackendAgent.db'; '{}' "
        final_command = formatted_command.format(sql_commands.replace("'", " \" "))
        print(final_command)
            
        process = subprocess.Popen(
            final_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=project_path,
            shell=True
        )

        output, error = process.communicate()            
        print("Command Output", output.decode('utf-8'), error.decode('utf-8'))
        return {
            "output":output.decode('utf-8'),
            "error":error.decode('utf-8')
        }
    
    def buildRequest(self, request):

        built_request = {
        'Method': request.method,
        'URL': request.url,
        'Headers': dict(request.headers),
        'Args': request.args if request.method == 'GET' else None,
        'JSON_Data': request.json if request.method == 'POST' else None,
        }

        return built_request
    
    
    def processResponseToFrontEnd(self, command_response):
        prompt = self.renderFronted(command_response, PROMPT_TO_FRONTEND)
        print("Frontedn Prompt", prompt)
        response = self.llm.inference(prompt)
        return response

    def execute(self, request):

        built_request = self.buildRequest(request)
        prompt = self.render(built_request, PROMPT_TO_DB)
        print(prompt)
        response = self.llm.inference(prompt)
        
        valid_response = self.validate_response(response)
        
        print("=====" * 10)
        print(valid_response)
        
        command_response = self.run_code(valid_response)
        response_to_frontend = self.processResponseToFrontEnd(command_response)
        print(response_to_frontend)
        response = response_to_frontend.strip().replace("```json", "```")
        
        if response.startswith("```") and response.endswith("```"):
            response = response[3:-3].strip()
        response = json.loads(response)

        return response