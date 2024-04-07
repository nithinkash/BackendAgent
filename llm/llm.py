from enum import Enum
from typing import List, Tuple

from .ollama_client import Ollama
from .claude_client import Claude
from .openai_client import OpenAI
from .groq_client import Groq

from state import AgentState

import tiktoken

from ..config import Config
from ..logger import Logger

TOKEN_USAGE = 0
TIKTOKEN_ENC = tiktoken.get_encoding("cl100k_base")

class Model(Enum):
    CLAUDE_3_OPUS = ("Claude 3 Opus", "claude-3-opus-20240229")
    CLAUDE_3_SONNET = ("Claude 3 Sonnet", "claude-3-sonnet-20240229")
    CLAUDE_3_HAIKU = ("Claude 3 Haiku", "claude-3-haiku-20240307")
    GPT_4_TURBO = ("GPT-4 Turbo", "gpt-4-0125-preview")
    GPT_3_5 = ("GPT-3.5", "gpt-3.5-turbo-0125")
    OLLAMA_MODELS = [
        (
            model["name"].split(":")[0],
            model["name"],
        )
        for model in Ollama.list_models()
    ]
    GROQ = ("GROQ Mixtral", "mixtral-8x7b-32768")


logger = Logger(filename="devika_prompts.log")

class LLM:
    def __init__(self, model_id: str = None):
        self.model_id = model_id
        self.log_prompts = Config().get_logging_prompts()
    
    def list_models(self) -> List[Tuple[str, str]]:
        return [model.value for model in Model if model.name != "OLLAMA_MODELS"] + list(
            Model.OLLAMA_MODELS.value
        )

    def model_id_to_enum_mapping(self):
        models = {model.value[1]: model for model in Model if model.name != "OLLAMA_MODELS"}
        ollama_models = {model[1]: "OLLAMA_MODELS" for model in Model.OLLAMA_MODELS.value}
        models.update(ollama_models)
        return models

    def update_global_token_usage(self, string: str, project_name: str):
        token_usage = len(TIKTOKEN_ENC.encode(string))
        AgentState().update_token_usage(project_name, token_usage)

    def inference(self, prompt: str) -> str:
        #self.update_global_token_usage(prompt, project_name)
        
        model = self.model_id_to_enum_mapping()[self.model_id]

        if self.log_prompts:
            logger.debug(f"Prompt ({model}): --> {prompt}")

        if model == "OLLAMA_MODELS":
            response = Ollama().inference(self.model_id, prompt).strip()
        elif "CLAUDE" in str(model):
            response = Claude().inference(self.model_id, prompt).strip()
        elif "GPT" in str(model):
            response = OpenAI().inference(self.model_id, prompt).strip()
        elif "GROQ" in str(model):
            response = Groq().inference(self.model_id, prompt).strip()
        else:
            raise ValueError(f"Model {model} not supported")

        if self.log_prompts:
            logger.debug(f"Response ({model}): --> {response}")

        #self.update_global_token_usage(response, project_name)
        
        return response
