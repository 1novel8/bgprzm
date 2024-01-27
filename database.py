import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
db_path = os.getenv('DB_PATH', None)
db_driver = 'DRIVER=Microsoft Access Driver (*.mdb, *.accdb)'
engine = create_engine(
    f'access+pyodbc://?odbc_connect={db_driver};'
    f'DBQ={db_path}'
)

session_maker = sessionmaker(bind=engine)
