import bcrypt
import requests
import oracledb
import os
from dotenv import load_dotenv
from typing import Optional
import datetime

load_dotenv()

class Database:
    def __init__(self, username, dsn, password):
        self.username = username
        self.dsn = dsn
        self.password = password
        
    def get_connection(self):
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
        
    def create_all_tables(self):
        tables = [
            (
                "CREATE TABLE USUARIOS("
                "id INTEGER PRIMARY KEY,"
                "username VARCHAR(32) UNIQUE,"
                "password VARCHAR(128)"
                ")"
            ),
            (
                "CREATE TABLE CONSULTAS("
                "id INTEGER PRIMARY KEY,"
                "nombre_indicador VARCHAR(50),"
                "fecha_indicador DATE,"
                "valor_indicador NUMBER(15,2),"
                "fecha_consulta TIMESTAMP,"
                "usuario_consulta VARCHAR(50)"
                ")"
            )
        ]

        for table in tables:
            self.query(table)

    def query(self, sql: str, parameters: Optional[dict] = None):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    ejecucion = cur.execute(sql, parameters)
                    if sql.startswith("SELECT"):
                        resultado = []
                        for fila in ejecucion:
                            resultado.append(fila)
                        return resultado
                conn.commit()
        except oracledb.DatabaseError as error:
            print(error)

class Auth:
    @staticmethod
    def login(db: Database, username: str, password: str):
        password = password.encode("UTF-8")

        resultado = db.query(
            sql= "SELECT * FROM USERS WHERE username = :username",
            parameters={"username":username}
        )

        if len(resultado) == 0:
            return print("No hay coincidencias")

        stored_hash = resultado[0][2]         
        stored_hash_bytes = stored_hash.encode("utf-8")

        if bcrypt.checkpw(password, stored_hash_bytes):
            return print("Logeado correctamente")
        else:
            return print("Contraseña incorrecta")

    @staticmethod
    def register(db: Database, id: int, username: str, password: str):
        print("registrando usuario")
        password = password.encode("UTF-8")
        salt = bcrypt.gensalt(12)
        hash_password = bcrypt.hashpw(password, salt).decode("utf-8")

        usuario = {
            "id": id,
            "username": username,
            "password": hash_password
        }

        db.query(
            sql= "INSERT INTO USUARIOS(id,username,password) VALUES (:id, :username, :password)",
            parameters=usuario
        )
        print("usuario registrado con exito")

class Finance:
    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url
        
    def get_indicator(self, indicator: str, fecha: str = None) -> float:
        try:
            if not fecha:
                dd = datetime.datetime.now().day
                mm = datetime.datetime.now().month
                yyyy = datetime.datetime.now().year
                fecha = f"{dd}-{mm}-{yyyy}"
            url = f"{self.base_url}/{indicator}/{fecha}"
            respuesta = requests.get(url).json()
            return respuesta["serie"][0]["valor"]
        except:
            print("Hubo un error con la solicitud")
            return 0.0
            
    def get_usd(self, fecha: str = None):
        valor = self.get_indicator("dolar", fecha)
        print(f"El valor del dolar en CLP es: {valor}")
        return valor
        
    def get_eur(self, fecha: str = None):
        valor = self.get_indicator("euro", fecha)
        print(f"El valor del euro en CLP es: {valor}")
        return valor
        
    def get_uf(self, fecha: str = None):
        valor = self.get_indicator("uf", fecha)
        print(f"El valor de la UF es: {valor}")
        return valor
        
    def get_ivp(self, fecha: str = None):
        valor = self.get_indicator("ivp", fecha)
        print(f"El valor del IVP es: {valor}")
        return valor
        
    def get_ipc(self, fecha: str = None):
        valor = self.get_indicator("ipc", fecha)
        print(f"El valor del IPC es: {valor}")
        return valor
        
    def get_utm(self, fecha: str = None):
        valor = self.get_indicator("utm", fecha)
        print(f"El valor de la UTM es: {valor}")
        return valor

def registrar_consulta(db: Database, usuario: str, indicador: str, fecha: str, valor: float):
    """Registra una consulta en la base de datos"""
    try:
        
        resultado = db.query("SELECT NVL(MAX(id), 0) + 1 FROM CONSULTAS")
        next_id = resultado[0][0] if resultado else 1
        
        consulta = {
            "id": next_id,
            "nombre_indicador": indicador,
            "fecha_indicador": fecha,
            "valor_indicador": valor,
            "fecha_consulta": datetime.datetime.now(),
            "usuario_consulta": usuario
        }
        
        db.query(
            sql="""
            INSERT INTO CONSULTAS 
            (id, nombre_indicador, fecha_indicador, valor_indicador, fecha_consulta, usuario_consulta)
            VALUES (:id, :nombre_indicador, TO_DATE(:fecha_indicador, 'DD-MM-YYYY'), 
                    :valor_indicador, :fecha_consulta, :usuario_consulta)
            """,
            parameters=consulta
        )
        
        print("✓ Consulta registrada")
        return True
        
    except Exception as e:
        print(f"⚠️ No se pudo registrar la consulta: {e}")
        return False

def ver_historial(db: Database, usuario: str):
    """Muestra el historial de consultas del usuario"""
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""
    =======================================
          HISTORIAL - {usuario}
    =======================================
    """)
    
    try:
        consultas = db.query(
            sql="""
            SELECT nombre_indicador, fecha_indicador, valor_indicador, fecha_consulta
            FROM CONSULTAS 
            WHERE usuario_consulta = :usuario
            ORDER BY fecha_consulta DESC
            """,
            parameters={"usuario": usuario}
        )
        
        if not consultas:
            print("No hay consultas registradas")
        else:
            print(f"Total de consultas: {len(consultas)}")
            print("-" * 60)
            
            for consulta in consultas:
                nombre, fecha_ind, valor, fecha_cons = consulta
                fecha_ind_str = fecha_ind.strftime("%d-%m-%Y") if fecha_ind else "N/A"
                fecha_cons_str = fecha_cons.strftime("%d-%m-%Y %H:%M") if fecha_cons else "N/A"
                
                print(f"{nombre}: {fecha_ind_str} = ${valor:,.2f} (consultado: {fecha_cons_str})")
            
            print("-" * 60)
            
    except Exception as e:
        print(f"Error al obtener historial: {e}")
    
    input("\nPresione ENTER para continuar...")


def menu_principal():
    db = Database(
        username=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )
    
    finanzas = Finance()
    usuario_actual = None
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        
        if not usuario_actual:
            print("""
            =======================================
                     SISTEMA DE INDICADORES
            =======================================
             1. INICIAR SESIÓN
             2. SALIR
            =======================================
            """)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                username = input("Usuario: ").strip()
                password = input("Contraseña: ").strip()
                
                
                resultado = db.query(
                    sql="SELECT * FROM USUARIOS WHERE username = :username",
                    parameters={"username": username}
                )
                
                if resultado:
                    usuario_actual = username
                    print(f"¡Bienvenido {usuario_actual}!")
                else:
                    print("Usuario no encontrado")
                input("\nPresione ENTER para continuar...")
                
            elif opcion == "2":
                try:
                    id = int(input("ID: ").strip())
                    username = input("Usuario: ").strip()
                    password = input("Contraseña: ").strip()
                    
                    Auth.register(db, id, username, password)
                    input("\nPresione ENTER para continuar...")
                except ValueError:
                    print("ID debe ser un número")
                    input("\nPresione ENTER para continuar...")
                    
            elif opcion == "3":
                print("Saliendo...")
                break
                
            else:
                print("Opción inválida")
                input("Presione ENTER para continuar...")
                
        else:
            
            print(f"""
            =======================================
                    SISTEMA DE INDICADORES
            =======================================
             1. CONSULTAR DÓLAR (USD)
             2. CONSULTAR EURO (EUR)
             3. CONSULTAR UF
             4. CONSULTAR IVP
             5. CONSULTAR IPC
             6. CONSULTAR UTM
             7. VER MI HISTORIAL
             8. CERRAR SESIÓN
            =======================================
            """)
            
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == "1":
                fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
                valor = finanzas.get_usd(fecha)
                
                
                if valor > 0:
                    if fecha:
                        fecha_consulta = fecha
                    else:
                        dd = datetime.datetime.now().day
                        mm = datetime.datetime.now().month
                        yyyy = datetime.datetime.now().year
                        fecha_consulta = f"{dd}-{mm}-{yyyy}"
                    
                    registrar_consulta(db, usuario_actual, "Dólar", fecha_consulta, valor)
                
                input("\nPresione ENTER para continuar...")
                
            elif opcion == "2":
                fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
                valor = finanzas.get_eur(fecha)
                
                if valor > 0:
                    if fecha:
                        fecha_consulta = fecha
                    else:
                        dd = datetime.datetime.now().day
                        mm = datetime.datetime.now().month
                        yyyy = datetime.datetime.now().year
                        fecha_consulta = f"{dd}-{mm}-{yyyy}"
                    
                    registrar_consulta(db, usuario_actual, "Euro", fecha_consulta, valor)
                
                input("\nPresione ENTER para continuar...")
                
            elif opcion == "3":
                fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
                valor = finanzas.get_uf(fecha)
                
                if valor > 0:
                    if fecha:
                        fecha_consulta = fecha
                    else:
                        dd = datetime.datetime.now().day
                        mm = datetime.datetime.now().month
                        yyyy = datetime.datetime.now().year
                        fecha_consulta = f"{dd}-{mm}-{yyyy}"
                    
                    registrar_consulta(db, usuario_actual, "UF", fecha_consulta, valor)
                
                input("\nPresione ENTER para continuar...")
                
            elif opcion == "4":
                fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
                valor = finanzas.get_ivp(fecha)
                
                if valor > 0:
                    if fecha:
                        fecha_consulta = fecha
                    else:
                        dd = datetime.datetime.now().day
                        mm = datetime.datetime.now().month
                        yyyy = datetime.datetime.now().year
                        fecha_consulta = f"{dd}-{mm}-{yyyy}"
                    
                    registrar_consulta(db, usuario_actual, "IVP", fecha_consulta, valor)
                
                input("\nPresione ENTER para continuar...")
                
            elif opcion == "5":
                fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
                valor = finanzas.get_ipc(fecha)
                
                if valor > 0:
                    if fecha:
                        fecha_consulta = fecha
                    else:
                        dd = datetime.datetime.now().day
                        mm = datetime.datetime.now().month
                        yyyy = datetime.datetime.now().year
                        fecha_consulta = f"{dd}-{mm}-{yyyy}"
                    
                    registrar_consulta(db, usuario_actual, "IPC", fecha_consulta, valor)
                
                input("\nPresione ENTER para continuar...")
                
            elif opcion == "6":
                fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
                valor = finanzas.get_utm(fecha)
                
                if valor > 0:
                    if fecha:
                        fecha_consulta = fecha
                    else:
                        dd = datetime.datetime.now().day
                        mm = datetime.datetime.now().month
                        yyyy = datetime.datetime.now().year
                        fecha_consulta = f"{dd}-{mm}-{yyyy}"
                    
                    registrar_consulta(db, usuario_actual, "UTM", fecha_consulta, valor)
                
                input("\nPresione ENTER para continuar...")
                
            elif opcion == "7":
                ver_historial(db, usuario_actual)
                
            elif opcion == "8":
                usuario_actual = None
                print("Sesión cerrada")
                input("Presione ENTER para continuar...")
                
            else:
                print("Opción inválida")
                input("Presione ENTER para continuar...")

if __name__ == "__main__":
    menu_principal()

