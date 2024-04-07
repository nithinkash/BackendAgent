import os

from config import Config
from logger import Logger

from bert.sentence import SentenceBert

def init_backendAgent():
    config = Config()
    logger = Logger()

    logger.info("Initializing BackendAgent...")
    sqlite_db = config.get_sqlite_db()
    logs_dir = config.get_logs_dir()

    logger.info("Initializing Prerequisites Jobs...")
    os.makedirs(os.path.dirname(sqlite_db), exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    

    logger.info("Loading sentence-transformer BERT models...")
    prompt = "Light-weight keyword extraction excercise for BERT model loading.".strip()
    SentenceBert(prompt).extract_keywords()
    logger.info("BERT model loaded successfully.")
