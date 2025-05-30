import os
from dotenv import load_dotenv

load_dotenv()

IMG_PATH = os.getenv('IMG_PATH')
SAVE_TO_PATH = os.getenv('SAVE_TO_PATH')