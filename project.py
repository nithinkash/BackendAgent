import os
import json
import zipfile
from datetime import datetime
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine

from config import Config

from llm import LLM

class Projects(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project: str
    message_stack_json: str

class ProjectManager:
    def __init__(self):
        config = Config()
        sqlite_path = config.get_sqlite_db()
        self.engine = create_engine(f"sqlite:///{sqlite_path}")
        SQLModel.metadata.create_all(self.engine)
        self.data = {
            "messages": []
        }

    def init_design(self, base_model):
        self.llm = LLM(model_id=base_model)
        self.prompt=" "
        while(1):
            self.response = self.llm.inference(prompt=self.prompt)
            print(self.response)
            self.data["messages"].append({
                "role": "BackendAgent",
                "content": self.response
            })
            self.input_from_user = input("User: ")
            if self.input_from_user == "exit":
                break
            self.prompt = self.input_from_user
            
            self.data["messages"].append({
                "role": "User",
                "content": self.input_from_user
            })
        
        with open(".assets/designChat.json", "w") as json_file:
            json.dump(self.data, json_file, indent=4)

            

    def new_message(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return {
            "from_backendAgent": True,
            "message": None,
            "timestamp": timestamp
        }

    def create_project(self, project: str):
        with Session(self.engine) as session:
            project_state = Projects(project=project, message_stack_json=json.dumps([]))
            session.add(project_state)
            session.commit()

    def delete_project(self, project: str):
        with Session(self.engine) as session:
            project_state = session.query(Projects).filter(Projects.project == project).first()
            if project_state:
                session.delete(project_state)
                session.commit()