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

def create_all_tables():
    tables = [
    (
        "CREATE TABLE mascotas ("
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
        "especie VARCHAR(32),"
        "vacunas_aplicada VARCHAR(100)"
        ")"
    ),
    (
        "CREATE TABLE gatos ("
        "id INTEGER PRIMARY KEY,"
        "nombre VARCHAR(64),"
        "edad Number(2),"
        "especie VARCHAR(32),"
        "fecha_esterilizacion VARCHAR(100)"
        ")"
    ),
        (
        "CREATE TABLE AVES ("
        "id INTEGER PRIMARY KEY,"
        "nombre VARCHAR(64),"
        "edad Number(2),"
        "especie VARCHAR(32),"
        "control_vuelo VARCHAR(100),"
        "tipo_jaula VARCHAR(100)"
        ")"
    )
]

    for query in tables:
        create_schema(query)


# PERSONAS
# Create - Inserción de datos
from datetime import datetime
def create_mascota(
        id: int,
        nombre: str,
        edad: int,
        especie: str
):
    sql = (
        "INSERT INTO MASCOTAS (id, nombre, edad, especie)"
        "VALUES (:id,:nombre,:edad,:especie)"
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

def create_perro(
        id: int,
        nombre: str,
        especie: str,
        vacunas_aplicada : str
):
    sql = (
        "INSERT INTO PERROS (id, nombre, especie, vacunas_aplicada)"
        "VALUES (:id,:nombre,:especie,:vacunas_aplicada)"
    )

    parametros = {
        "id": id,
        "nombre": nombre,
        "especie": especie,
        "vacunas_aplicada": vacunas_aplicada
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

def create_gato(
        id: int,
        nombre: str,
        edad: int,
        especie: str,
        fecha_esterilizacion : str,
):
    sql = (
        "INSERT INTO GATOS (id, nombre,edad,especie, fecha_esterilizacion)"
        "VALUES (:id,:nombre,:edad,:especie,:fecha_esterilizacion)"
    )
        
    parametros = {
        "id": id,
        "nombre": nombre,
        "edad": edad,
        "especie": especie,
        "fecha_esterilizacion":fecha_esterilizacion, 
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

def create_ave(
        id: int,
        nombre: str,
        edad: int,
        especie: str,
        control_vuelo : str,
        tipo_jaula : str
):
    sql = (
        "INSERT INTO AVES (id, nombre, edad, especie, control_vuelo, tipo_jaula)"
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
    
def read_mascota_by_id(id):
    sql = (
        "SELECT * FROM MASCOTAS WHERE id = :id"
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

def read_perro_by_id(id):
    sql = (
        "SELECT * FROM PERROS WHERE id = :id"
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


def read_gato_by_id(id):
    sql = (
        "SELECT * FROM GATOS WHERE id = :id"
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

def read_ave_by_id(id):
    sql = (
        "SELECT * FROM AVES WHERE id = :id"
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
def update_mascota(
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
        modificaciones.append("especie =: especie")
        parametros["especie"] = especie
    if not modificaciones:
        return print("No hay campos para actualizar.")

    sql = f"UPDATE mascotas SET {", ".join(modificaciones)} WHERE id =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Persona con nombre={nombre} actualizada.") 

def update_perro(
    id,
    nombre: Optional[str] = None,
    especie: Optional[str] = None,
    vacunas_aplicada: Optional[str] = None,
    
):
    modificaciones = []
    parametros = {"id": id}

    if nombre is not None:
        modificaciones.append("nombre =: nombre")
        parametros["nombre"] = nombre
    if vacunas_aplicada is not None:
        modificaciones.append("vacunas_aplicada =: vacunas_aplicada")
        parametros["vacunas_aplicada"] = vacunas_aplicada
    if especie is not None:
        modificaciones.append("especie = :especie")
        parametros["especie"] = especie
    if not modificaciones:
        return print("No hay campos para actualizar.")

    sql = f"UPDATE perros SET {", ".join(modificaciones)} WHERE id =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Persona con nombre={nombre} actualizada.") 

def delete_mascota(id: int):
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

def update_gato(
    id,
    nombre: Optional[str] = None,
    edad: Optional[str] = None,
    especie: Optional[str] = None,
    fecha_esterilizacion: Optional[str] = None,
    
):
    modificaciones = []
    parametros = {"id": id}

    if nombre is not None:
        modificaciones.append("nombre =: nombre")
        parametros["nombre"] = nombre
    if fecha_esterilizacion is not None:
        modificaciones.append("fecha_esterilizacion =: fecha_esterilizacion")
        parametros["fecha_esterilizacion"] = fecha_esterilizacion
    if edad is not None:
        modificaciones.append("edad =: edad")
        parametros["edad"] = edad
    if especie is not None:
        modificaciones.append("espeice =: especie")
        parametros["especie"] = especie
    if not modificaciones:
        return print("No hay campos para actualizar.")

    sql = f"UPDATE gatos SET {", ".join(modificaciones)} WHERE id =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Persona con nombre={nombre} actualizada.") 

def delete_perro(id: int):
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

def update_ave(
    id,
    nombre: Optional[str] = None,
    edad: Optional[str] = None,
    especie: Optional[str] = None,
    tipo_jaula: Optional[str] = None,
    control_vuelo: Optional[str] = None,
    
):
    modificaciones = []
    parametros = {"id": id}

    if nombre is not None:
        modificaciones.append("nombre =: nombre")
        parametros["nombre"] = nombre
    if edad is not None:
        modificaciones.append("edad =: edad")
        parametros["edad"] = edad
    if tipo_jaula is not None:
        modificaciones.append("tipo_jaula =: tipo_jaula")
        parametros["tipo_jaula"] = tipo_jaula
    if control_vuelo is not None:
        modificaciones.append("control_vuelo =: control_vuelo")
        parametros["control_vuelo"] = control_vuelo
    if especie is not None:
        modificaciones.append("espeice =: especie")
        parametros["especie"] = especie
    if not modificaciones:
        return print("No hay campos para actualizar.")

    sql = f"UPDATE aves SET {", ".join(modificaciones)} WHERE id =: id"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
        conn.commit()
        print(f"Persona con nombre={nombre} actualizada.") 

def delete_gato(id: int):
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

def delete_ave(id: int):
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


def menu_mascotas():
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

        opcion = input("Selecciona una opcion [1-5, 0 para volver al menu principal]:")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id = int(input("Ingrese el id numerico de la mascota: "))
                nombres = input("Ingrese nombres de la mascota: ")
                edad = int(input("Ingrese la edad: "))
                especie = input("Ingresa la especie: ")
                create_mascota(id,nombres,edad,especie)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_mascotas()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id = int(input("Ingrese el id numerico de la mascota: "))
                read_mascota_by_id(id)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id = int(input("Ingrese el id numerico de la mascota: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                nombres = input("Ingrese nombres de la mascota: ")
                especie = input("Ingresa la especie: ")
                edad = int(input("Ingrese la edad"))
                if len(nombres.strip()) == 0:
                    nombres = None
                if len(especie.strip()) == 0:
                    especie = None
                if len(edad.strip()) == 0:
                    edad = None
                update_mascota(id,nombres,especie,edad)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id = int(input("Ingrese el id numerico de la persona: "))
                delete_mascota(id)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break

def menu_perros():
    while True:
        os.system("cls")
        print(
            """
            =======================================
                         MENU PERROS 
            =======================================
             1. INSERTAR PERROS
             2. LEER PERROS
             3. LEER PERROS POR ID
             4. MODIFICAR PERROS 
             5. ELIMINAR PERROS
             0. SALIR
            ======================================

            """
        )
        opcion = input("Selecciona una opcion [1-5, 0 para volver al menu principal]:")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id = int(input("Ingrese el id numerico del perro: "))
                nombres = input("Ingrese nombres del perro: ")
                especie = input("Ingrese la raza: ")
                vacunas_aplicada = str(input("Ingrese vacunas aplicada: "))
                create_perro(id,nombres,especie,vacunas_aplicada)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_perros()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id = int(input("Ingrese el id numerico del perro: "))
                read_perro_by_id(id)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id = int(input("Ingrese el id numerico del perro: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                nombres = input("Ingrese nombres del perro: ")
                especie = input("Ingresa la especie: ")
                vacunas_aplicada = input("Ingrese las vacunas aplicadas: ")
                if len(nombres.strip()) == 0:
                    nombres = None
                if len(especie.strip()) == 0:
                    especie = None
                if len(vacunas_aplicada.strip()) == 0:
                    vacunas_aplicada = None
                update_perro(id,nombres,especie,vacunas_aplicada)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id = int(input("Ingrese el id numerico del perro: "))
                delete_perro(id)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break

def menu_gatos():
    while True:
        os.system("cls")
        print(
            """
            =======================================
                         MENU GATOS 
            =======================================
             1. INSERTAR GATOS
             2. LEER GATOS
             3. LEER GATOS POR ID
             4. MODIFICAR GATOS 
             5. ELIMINAR GATOS
             0. SALIR
            ======================================

            """
        )

        opcion = input("Selecciona una opcion [1-5, 0 para volver al menu principal]:")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id = int(input("Ingrese el id numerico del gato: "))
                nombre = input("Ingrese nombres del gato: ")
                edad = int(input("Ingrese la edad: "))
                especie = input("Ingrese la raza: ")
                fecha_esterilizacion = input("Ingrese la fecha de esterilizacion: ")
                create_gato(id,nombre,edad,especie,fecha_esterilizacion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_gatos()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id = int(input("Ingrese el id numerico del gato: "))
                read_gato_by_id(id)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id = int(input("Ingrese el id numerico del gato: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                nombre = input("Ingrese nombres del gato: ")
                especie = input("Ingresa la especie: ")
                edad = int(input("Ingrese la edad: "))
                fecha_esterilizacion = ("Ingrese la fecha de esterilizacion")
                if len(nombres.strip()) == 0:
                    nombres = None
                if len(especie.strip()) == 0:
                    especie = None
                if len(fecha_esterilizacion.strip()) == 0:
                    fecha_esterilizacion = None
                if len(edad.strip()) == 0:
                    edad = None
                update_gato(id,nombre,edad,especie,fecha_esterilizacion)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id = int(input("Ingrese el id numerico del gatl ave: "))
                delete_gato(id)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break


def menu_aves():
    while True:
        os.system("cls")
        print(
            """
            =======================================
                         MENU AVES 
            =======================================
             1. INSERTAR AVES
             2. LEER AVES
             3. LEER MAVES POR ID
             4. MODIFICAR AVES 
             5. ELIMINAR AVES
             0. SALIR
            ======================================

            """
        )

        opcion = input("Selecciona una opcion [1-5, 0 para volver al menu principal]:")

        if opcion == "0":
            os.system("cls")
            print("Volviendo al menú principal")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            try:
                id = int(input("Ingrese el id numerico del ave: "))
                nombres = input("Ingrese nombres del ave: ")
                edad = int(input("Ingrese la edad: "))
                especie = input("Ingresa la raza: ")
                control_vuelo = input("Ingrese el cotrol de vuelo: ")
                tipo_jaula = input("Ingrese el tipo de jaula: ")
                create_ave(id,nombres,edad,especie,control_vuelo,tipo_jaula)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            read_aves()
            input("Presiona ENTER para continuar...")
        elif opcion == "3":
            try:
                id = int(input("Ingrese el id numerico del ave: "))
                read_ave_by_id(id)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        elif opcion == "4":
            try:
                id = int(input("Ingrese el id numerico del ave: "))
                print("⚠️ Sólo digite cuándo quiera modificar el dato")
                nombres = input("Ingrese nombres del ave: ")
                especie = input("Ingresa la especie: ")
                control_vuelo = input("Ingrese el cotrol de vuelo")
                tipo_jaula = input("Ingrese el tipo de jaula")
                edad = input("Ingrese la edad")
                if len(nombres.strip()) == 0:
                    nombres = None
                if len(especie.strip()) == 0:
                    especie = None
                if len(control_vuelo.strip()) == 0:
                    control_vuelo = None
                if len(tipo_jaula.strip()) == 0:
                    tipo_jaula = None
                if len(edad.strip()) == 0:
                    edad = None
                update_ave(id,nombres,edad,especie,tipo_jaula,control_vuelo)
            except ValueError:
                print("Ingresaste un valor no númerico")

            input("Presiona ENTER para continuar...")
        elif opcion == "5":
            try:
                id = int(input("Ingrese el id numerico del ave: "))
                delete_ave(id)
            except ValueError:
                print("Ingresaste un valor no númerico")
            
            input("Presiona ENTER para continuar...")
        else:
            print("Opción invalida")
            input("Presiona ENTER para continuar...")
            break


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
        opcion = input("Selecciona una opcion [1=5, 0 para salir]: ")

        if opcion == "0":
            print("Adios")
            input("Presiona ENTER para continuar...")
            break
        elif opcion == "1":
            create_all_tables()
            input("Presiona ENTER para continuar...")
        elif opcion == "2":
            menu_mascotas()
            input("Presiona ENTER para continuar  ")
        elif opcion == "3":
            menu_perros()
            input("Presiona ENTER para continuar  ")
        elif opcion == "4":
            menu_gatos()
            input("Presiona ENTER para continuar  ")
        elif opcion == "5":
            menu_aves()
            input("Presiona ENTER para continuar  ")

if __name__ == "__main__":
    main("cls")