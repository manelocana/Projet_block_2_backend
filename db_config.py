

import os
import mysql.connector
from dotenv import load_dotenv



load_dotenv()


DB_CONFIG = {
    "host": os.environ["DB_HOST"],       
    "user": os.environ["DB_USER"],       
    "password": os.environ["DB_PASS"],   
    "database": os.environ["DB_NAME"],   
    "port": int(os.environ.get("DB_PORT", 3306)),  
}



def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)