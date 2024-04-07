from logger import Logger

from .runner import Runner
from config import Config

class Agent:
    def __init__(self, base_model):
        if not base_model:
            raise ValueError("base_model is required")
        
        self.logger = Logger()
        self.config = Config()

        #Runner Agent
        self.runner = Runner(base_model=base_model) 

    def execute(self, ):
        