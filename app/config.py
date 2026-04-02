import os
import sys
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.curdir)
sys.path.insert(0, BASE_DIR)

load_dotenv()

mercadopago_access_token = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
database_url = os.getenv('DATABASE_URL')