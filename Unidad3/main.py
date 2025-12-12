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
import datetime
#Cargar las variables desde el archivo .env
load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

class Database:
        def __init__(self,username,password,dsn):
                self.username=username
                self.password=password
                self.dsn=dsn
        def get_connection(self):
                return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
        def create_all_tables(self):
                pass
        def query(self, sql, parameters: Optional[dict]):
            try:
                with self.get_connection() as conn:
                    with conn.cursor() as cur:
                        resultado = cur.execute(sql, parameters)
                        return resultado
                    conn.commit()
            except oracledb.DatabaseError as error:
                print(error)


class Auth:
        staticmethod
        def login(db: Database, username: str, password: str):
                pass
        staticmethod
        def register(db: Database, username: str, password: str):
                pass

"""
DOLAR
EURO
UD
IVP
IPC
UTM
"""


class Finance:
        def __init__(self, base_url: str = "https://mindicador.cl/api"):
            self.base_url = base_url
        def get_indicator (self, indicator: str, fecha: None, ) -> int:
            try:
                if not fecha:    
                    dd = datetime.datetime.now().day
                    mm = datetime.datetime.now().month
                    yyyy = datetime.datetime.now().year
                    fecha = f"{dd}-{mm}-{yyyy}"  
                url = f"{self.base_url}/{indicator}/{fecha}"
                respuesta = requests.get(url).json()
                print(respuesta["serie"][0]["valor"])
            except:
                  print("Hubo un error con la solicitud")
        def get_usd (self, fecha: str = None):
            valor = self.get_indicator("dolar",fecha)
            print(f"El valor del dolar en CLP es: {valor}")
        def get_eur (self, fecha: str = None):
            self.get_indicator("eur",fecha)
        def get_uf (self, fecha: str = None):
            self.get_indicator("uf",fecha)
        def get_uf (self, fecha: str = None):
            self.get_indicator("ivp",fecha)
        def get_uf (self, fecha: str = None):
            self.get_indicator("utm",fecha)
    
if __name__ == "__main__":
    indicadores = Finance()
    indicadores.get_usd("28-11-2025")

if __name__ == "__main__":        
    db = Database(
       username=os.getenv("ORACLE_USER"),
       password=os.getenv("ORACLE_PASSWORD"),
       dsn=os.getenv("ORACKE_DSN")
    )
    print(db.query(sql="SELECT sysdate FROM dual"))