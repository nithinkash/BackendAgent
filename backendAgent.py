from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from logger import Logger, route_logger
import uuid

from init import init_backendAgent

app = Flask(__name__)
log = logging.getLogger("werkzeug")
log.disabled = True
CORS(app)

logger = Logger()

@app.route("/api/create", methods=["POST"])
@route_logger(logger)
def postData():
    requestId = str(uuid.uuid1())
    data = request.json
    return jsonify({"message": "Message frrm the LLM"})
    
@app.route("/api/retrieve", methods=["GET"])
@route_logger(logger)
def getData():
    requestId = str(uuid.uuid1())
    return jsonify({"data":"From LLM"})

if __name__ == "__main__":
    logger.info("Booting up... This may take a few seconds")
    init_backendAgent()
    app.run(debug=False, port=1337, host="0.0.0.0")