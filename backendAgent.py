from flask import Flask, request
from flask_cors import CORS
import logging
from logger import Logger, route_logger
from config import Config
import os
import shutil

from init import init_backendAgent
from project import init_design
from agents.designer.designer import Designer
from agents.runner import Runner

app = Flask(__name__)
log = logging.getLogger("werkzeug")
log.disabled = True
BASE_MODEL="gpt-3.5-turbo"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
CORS(app)

logger = Logger()
config = Config()

@app.route("/api/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@route_logger(logger)
def apiGateway(path):
    runner = Runner(base_model=BASE_MODEL)
    response = runner.execute(request=request)
    return response 

if __name__ == "__main__":
    logger.info("Booting up... This may take a few seconds")
    init_backendAgent()
    if not os.path.isfile("config.toml"):
        shutil.copy(".asset/config.toml", os.getcwd())
        input("Please set the config.toml file and press enter")
    if not os.path.isfile(os.path.join(os.getcwd(),".assets/designChat.json")):
       init_design(BASE_MODEL)
       designer = Designer(base_model=BASE_MODEL)
       designer.execute()
    app.run(debug=True, port=25680, host="0.0.0.0", use_reloader=False)