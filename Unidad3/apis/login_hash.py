import os
import bcrypt
import oracledb
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(
        user=username,
        password=password,
        dsn=dsn
    )
        
incoming_password = input("Ingresa una contraseña: ").encode("UTF-8")
salt = bcrypt.gensalt(rounds=12)
hashed_password = bcrypt.hashpw(incoming_password,salt)

print(f"Cotraseña obtenida: {incoming_password}")
print(f"Contraseña hasheada: {hashed_password}")