# Dependencias:
# pip install oracledb python-dotenv bcrypt
import os
import bcrypt
import oracledb
# Cargamos las variables de entorno desde .env
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

def create_table_users():
    query = (
        "CREATE TABLE USUARIOS ("
        "id INTEGER PRIMARY KEY,"
        "username VARCHAR2(16) NOT NULL UNIQUE,"
        "password VARCHAR2(128) NOT NULL"
        ")"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                print(f"Tabla creada \n {query}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la tabla: {err} \n {query}")

# Paso 1. Obtengo la contraseña 🧷
new_username = input("Ingresa un nombre de usuario: ")
incoming_password = input("Ingresa una contraseña: ").encode("UTF-8")
# Paso 2. Genero la sal 🧂
salt = bcrypt.gensalt(rounds=12)
# Paso 3. Hasheo la contraseña con la sal generada 🧑‍💻
hashed_password_bytes = bcrypt.hashpw(incoming_password, salt)
hashed_password_string = hashed_password_bytes.decode('utf-8')  # <-- CORRECCIÓN

print(f"Contraseña obtenida: {incoming_password}")
print(f"Contraseña hasheada (bytes): {hashed_password_bytes}")
print(f"Contraseña hasheada (string): {hashed_password_string}")
print(f"Largo del hash: {len(hashed_password_string)}")


# Paso 4. Guardarlo en la base de datos
create_table_users()

query = (
    "INSERT INTO USUARIOS(id, username, password)"
    "VALUES (:id, :username, :password)"
)

parametros = {
    "id": 1,
    "username": new_username,
    "password": hashed_password_string  # <-- CORRECCIÓN
}

try:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, parametros)
            print(f"Ejecución lista \n {query}")
        conn.commit()
except oracledb.DatabaseError as e:
    err = e
    print(f"No se pudo ejecutar: {err} \n {query}")