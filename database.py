from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_path = r'D:\projects\bgprz\DKR.mdb'
db_driver = 'DRIVER=Microsoft Access Driver (*.mdb, *.accdb)'
engine = create_engine(
    f'access+pyodbc://?odbc_connect={db_driver};'
    f'DBQ={db_path}'
)

session_maker = sessionmaker(bind=engine)
