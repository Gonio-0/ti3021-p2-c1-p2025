# Importamos librerias
import oracledb
import os
from dotenv import load_dotenv
# Cargamos variables de entorno
load_dotenv()
# Definimos valores gracias a las variables de entorno
username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")
# Creamos una conexion reutilizable
def get_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)

# Funcion para crear el esquema de la base de datos
def create_schema(query):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                print(f"Tabla creada \n {query}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la tabla: {err} \n {query}")

tables = [
    (
        "CREATE TABLE mascotas ("
        "id INTEGER PRIMARY KEY,"
        "nombre VARCHAR(64) NOT NULL,"
        "edad INTEGER NOT NULL,"
        "especie VARCHAR(32) NOT NULL,"
        ")"
    ),
   (
        "CREATE TABLE perros ("
        "id INTEGER PRIMARY KEY,"
        "id_mascota INTEGER NOT NULL,"
        "vacunas_aplicadas VARCHAR(255),"
        "FOREIGN KEY (id_mascota) REFERENCES mascotas(id)"
        ")"
    ),
    (
        "CREATE TABLE gatos ("
        "id INTEGER PRIMARY KEY,"
        "id_mascota INTEGER NOT NULL,"
        "fecha_esterilizacion DATE,"
        "FOREIGN KEY (id_mascota) REFERENCES mascotas(id)"
        ")"
    ),
       (
        "CREATE TABLE aves ("
        "id INTEGER PRIMARY KEY,"
        "id_mascota INTEGER NOT NULL,"
        "control_vuelo VARCHAR(50),"
        "tipo_jaula VARCHAR(50),"
        "FOREIGN KEY (id_mascota) REFERENCES mascotas(id)"
        ")"
    ),
]

for query in tables:
    create_schema(query)

def create_mascota(
        id: int,
        nombres: str,
        edad: int,
        especie: str
):
    sql = (
        "INSERT INTO MASCOTAS (id,nombres,edad,especie)" \
        "VALUES (:id,:nombres,:edad,:especie"
    )
    
    parametros = (
        "id" : id,


    )

def create_perros(
        id: int,
        nombres: str,
        edad: int,
        especie: str,
        vacunas_aplicadas: str
):
    pass

def create_gatos(
        id: int,
        nombres: str,
        edad: int,
        especie: str,
        fecha_esterilizacion: int
):
    pass

def create_gatos(
        id: int,
        nombres: str,
        edad: int,
        especie: str,
        control_vuelo: str,
        tipo_jaula: str
):
    pass

# from datetime import datetime
# # CREATE
# def create_persona(rut, nombres, apellidos=None, fecha_nacimiento=None, cod_area="+569", numero_telefono=None):
#     sql = (
#     "INSERT INTO personas (rut, nombres, apellidos, fecha_nacimiento, cod_area, numero_telefono) "
#     "VALUES (:rut, :nombres, :apellidos, :fecha_nacimiento, :cod_area, :numero_telefono)"
#     )
#     if fecha_nacimiento:
#         bind_fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
#     else:
#         bind_fecha = None
#     with get_connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute(sql, {
#             "rut": rut,
#             "nombres": nombres,
#             "apellidos": apellidos,
#             "fecha_nacimiento": bind_fecha,
#             "cod_area": cod_area,
#             "numero_telefono": numero_telefono,
#             })
#         conn.commit()
#     print(f"Persona con RUT={rut} creada.")
# create_persona(
#     rut="12314984-9",
#     nombres="Roberto Mandril",
#     apellidos="Manda Jara"
# )
# # READ
# def list_personas(limit: int = 100):
#     sql = f"SELECT * FROM personas FETCH FIRST {limit} ROWS ONLY"
#     results = []
#     with get_connection() as conn:
#         with conn.cursor() as cur:
#             cur.execute(sql)
#             for row in cur:
#                 rut, nombres, apellidos, fecha_nacimiento, cod_area, numero_telefono = row
#                 results.append({
#                 "rut": rut,
#                 "nombres": nombres,
#                 "apellidos": apellidos,
#                 "fecha_nacimiento": fecha_nacimiento.isoformat() if fecha_nacimiento else None,
#                 "cod_area": cod_area,
#                 "numero_telefono": numero_telefono,
#                 })
#     return results
# print(list_personas())