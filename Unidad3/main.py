#conecion a la base de datos
import oracledb
import os
from dotenv import load_dotenv
#Hasheo de cpmtraseñas
import bcrypt
#Comsumo de APU
import requests
#parametros opcionales
from typing import Optional

#Cargar las variables desde el archivo .env
load_dotenv()

class Database:
        def __init__(self,username,password,dsn):
                self.username=username
                self.password=password
                self.dsn=dsn
        def get_connection(self):
                return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
        def create_all_tables(self):
                pass
        def query(self, sql, parameters: optional[dict] = None):
            print(f"ejecutando query:\n{sql}\n{parameters}")
            try:
                with self.get_connection() as conn:
                    with conn.cursor() as cur:
                        resultados = cur.execute(statement=sql, parameters=parameters)
                        for fila in resultados:
                        print(fila)


class Auth:
        staticmethod
        def login(db: Database, username: str, password: str):
                pass
        staticmethod
        def register(db: Database, username: str, password: str):
                pass

class Finance:
        def __init__(self, base_url: str):
            self.base_url = base_url
        def get_uf (self):
            pass
        def get_uf (self):
            pass
        def get_uf (self):
            pass
        def get_uf (self):
            pass
        def get_uf (self):
            pass
        def get_uf (self):
            pass
    

if __name__ == "__main__":        
    db = Database(
       username=os.getenv("ORACLE_USER"),
       password=os.getenv("ORACLE_PASSWORD"),
       dsn=os.getenv("ORACKE_DSN")
    )

db.query(sql="SELECT sysdate FROM dual")