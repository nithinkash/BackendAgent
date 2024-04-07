from llm import LLM

class Designer:
    def __init__(self, base_model) -> None:
        self.llm = LLM(model_id=base_model)
        self.conversations = None

    
    