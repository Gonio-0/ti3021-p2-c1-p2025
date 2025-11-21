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
        print(f"No se pudo crear la datos: {err}")
    
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
        print(f"No se pudo crear la datos: {err}")

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
        print(f"No se pudo crear la datos: {err}")

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
        print(f"No se pudo crear la datos: {err}")

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
        print(f"No se pudo crear la datos: {err}")


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
        print(f"No se pudo crear la datos: {err}")

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
        print(f"No se pudo crear la datos: {err}")

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
        print(f"No se pudo crear la datos: {err}")

from typing import Optional
def update_mascotas(
    id,
    nombre: Optional[str] = None,
    edad: Optional[str] = None,
    especie: Optional[str] = None,
    
):
    modificaciones = []
    parametros = {"id": id}

    if nombre is not None:
        modificaciones.append("nombre =: nombre")
        parametros["nombre"] = nombre
    if edad is not None:
        modificaciones.append("edad =: edad")
        parametros["edad"] = edad
    if especie is not None:
        modificaciones.append("espeice =: especie")
        parametros["especie"] = especie
    if not modificaciones:
        return print("No hay campos para actualizar.")

    sql = f"UPDATE mascotas SET {", ".join(modificaciones)} WHERE id =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Persona con nombre={nombre} actualizada.") 

def delete_mascotas(id: int):
    sql = (
        "DELETE FROM MASCOTAS WHERE id = :id"
    )

    parametros = {"id" : id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                conn.commit()
                print(f"Dato eliminado \n {parametros} ")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Errormal eliminar dato: {err} \n {sql} \n {parametros}:")

def delete_perros(id: int):
    sql = (
        "DELETE FROM PERROS WHERE id = :id"
    )

    parametros = {"id" : id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                conn.commit()
                print(f"Dato eliminado \n {parametros} ")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Errormal eliminar dato: {err} \n {sql} \n {parametros}:")

def delete_gatos(id: int):
    sql = (
        "DELETE FROM GATOS WHERE id = :id"
    )

    parametros = {"id" : id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                conn.commit()
                print(f"Dato eliminado \n {parametros} ")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Errormal eliminar dato: {err} \n {sql} \n {parametros}:")

def delete_AVES(id: int):
    sql = (
        "DELETE FROM AVES WHERE id = :id"
    )

    parametros = {"id" : id}

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
                conn.commit()
                print(f"Dato eliminado \n {parametros} ")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Errormal eliminar dato: {err} \n {sql} \n {parametros}:")


def menu_mascota():
    while True:
        os.system("cls")
        print(
            """
            =======================================
                         MENU MASCOTAS 
            =======================================
             1. INSERTAR MASCOTAS
             2. LEER MASCOTAS
             3. LEER MASCOTA POR ID
             4. MODIFICAR MASCOTAS 
             5. ELIMINAR MASCOTAS
             0. SALIR
            ======================================

            """
        )

def main(cls):
    while True:
        os.system(cls)
        print(
            """
            =======================================
                       CRUD CON ORACLESQL
            =======================================
             1. APLICAR ESQUEMA EN LA BASE DE DATOS
             2. TABLA MASCOTAS
             3. TABLA PERROS
             4. TABLA GATOS
             5. TABLA AVES
             0. SALIR
            ======================================
            
            """
        )
        opcion = input("Selecciona una pcion [1=5, 0 para salir]")

        if opcion == "0":
            print("Adios")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id = input("Ingrese el id numerico de la mascota: ")
                nombre = input("Ingrese el id numerico de la mascota: ")
                especie = input("Ingrese el id numerico de la mascota: ")
            except ValueError:
                return print("ingresaste un valor no numerico")

            create_mascotas(id,nombre,especie)
            input("Presiona ENTER para continuar  ")

        elif opcion == "2":
            pass
        elif opcion == "3":
            pass
        elif opcion == "4":
            pass
        elif opcion == "5":
            pass

if __name__ == "__name__":
    main()