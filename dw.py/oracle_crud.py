import oracledb
import os
from dotenv import load_dotenv
load_dotenv()
username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)

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
        "CREATE TABLE mascota ("
        "id INTEGER PRIMARY KEY,"
        "nombre VARCHAR(64),"
        "edad Number(2),"
        "especie VARCHAR(32)"
        ")"
    ),
    (
        "CREATE TABLE perros ("
        "id INTEGER PRIMARY KEY,"
        "nombre VARCHAR(64),"
        "especie VARCHAR(32)"
        "vacunas_aplicada VARCAHR(100"
        ")"
    ),
    (
        "CREATE TABLE gatos ("
        "id INTEGER PRIMARY KEY,"
        "nombre VARCHAR(64),"
        "edad Number(2),"
        "especie VARCHAR(32),"
        "fecha_esterilizacion VARCHAR(100),"
        ")"
    ),
        (
        "CREATE TABLE AVES ("
        "id INTEGER PRIMARY KEY,"
        "nombre VARCHAR(64),"
        "edad Number(2),"
        "especie VARCHAR(32),"
        "control_vuelo VARCHAR(100),"
        "tipo_jaula VARCHAR"
        ")"
    )
]

for query in tables:
    create_schema(query)


# PERSONAS
# Create - Inserción de datos
from datetime import datetime
def create_mascotas(
        id: int,
        nombre: str,
        edad: int,
        especie: str
):
    sql = (
        "INSERT INTO MASCOTAS (id, nombre, edad, especie)"
        "VALUES (:id,:nombre,:edad,:especie,)"
    )

    parametros = {
        "id": id,
        "nombre": nombre,
        "edad": edad,
        "especie": especie,
    }

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql,parametros)
                print(f"Dato insertado \n {parametros}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err} \n {parametros}")

def create_perros(
        id: int,
        nombre: str,
        edad: int,
        especie: str,
        vacunas_aplicadas : str
):
    sql = (
        "INSERT INTO PERROS (id, nombre, edad, especie, vacunas_aplicadas)"
        "VALUES (:id,:nombre,:edad,:especie,:vacunas_aplicadas)"
    )

    parametros = {
        "id": id,
        "nombre": nombre,
        "edad": edad,
        "especie": especie,
        "vacunas_aplicadas": vacunas_aplicadas
    }

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql,parametros)
                print(f"Dato insertado \n {parametros}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err} \n {parametros}")

def create_gatos(
        id: int,
        nombre: str,
        edad: int,
        especie: str,
        fecha_esterilizacion : str
):
    sql = (
        "INSERT INTO GATOS (id, nombre, edad, especie, fecha_esterilizacion)"
        "VALUES (:id,:nombre,:edad,:especie,:fecha_esterilizacion)"
    )
        
    parametros = {
        "id": id,
        "nombre": nombre,
        "edad": edad,
        "especie": especie,
        "fechas_esterilizacion":fecha_esterilizacion
    }
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql,parametros)
                print(f"Dato insertado \n {parametros}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err} \n {parametros}")    

def create_aves(
        id: int,
        nombre: str,
        edad: int,
        especie: str,
        control_vuelo : str,
        tipo_jaula : str
):
    sql = (
        "INSERT INTO AVES (id, nombre, edad, especie, control_vuelo, tipo_jauña)"
        "VALUES (:id,:nombre,:edad,:especie,:control_vuelo,:tipo_jaula)"
    )
        
    parametros = {
        "id": id,
        "nombre": nombre,
        "edad": edad,
        "especie": especie,
        "control_vuelo": control_vuelo,
        "tipo_jaula": tipo_jaula
    }
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql,parametros)
                print(f"Dato insertado \n {parametros}")
            conn.commit()
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al insertar datos: {err} \n {parametros}")    
    


def read_mascotas():
    sql = (
        "SELECT * FROM MASCOTAS"
    )    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print(f"Consulta a la tabla MASCOTAS")
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la datos:")
    
def read_mascotas_by_id(id):
    sql = (
        "SELECT * FROM MASCOTAS WHERE id"
    )    

    parametros = {"id":id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print(f"Consulta a la tabla MASCOTAS por ID")
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la datos:")

def read_perros():
    sql = (
        "SELECT * FROM PERROS"
    )    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print(f"Consulta a la tabla PERROS")
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la datos:")

def read_perros_by_id(id):
    sql = (
        "SELECT * FROM PERROS WHERE id"
    )    

    parametros = {"id":id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print(f"Consulta a la tabla PERROS por ID")
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la datos:")

def read_gatos():
    sql = (
        "SELECT * FROM GATOS"
    )    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print(f"Consulta a la tabla GATOS")
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la datos:")


def read_gatos_by_id(id):
    sql = (
        "SELECT * FROM GATOS WHERE id"
    )    

    parametros = {"id":id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print(f"Consulta a la tabla GATOS por ID")
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la datos:")

def read_aves():
    sql = (
        "SELECT * FROM AVES"
    )    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql)
                print(f"Consulta a la tabla AVES")
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la datos:")

def read_aves_by_id(id):
    sql = (
        "SELECT * FROM AVES WHERE id"
    )    

    parametros = {"id":id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                resultados = cur.execute(sql,parametros)
                print(f"Consulta a la tabla AVES por ID")
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la datos:")