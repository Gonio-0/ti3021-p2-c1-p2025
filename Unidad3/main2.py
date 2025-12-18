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
                "CREATE TABLE USERS("
                "id INTEGER PRIMARY KEY,"
                "username VARCHAR(32) UNIQUE,"
                "password VARCHAR(128)"
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
            print(f"Error en la consulta: {error}")

class Auth:
    @staticmethod
    def login(db: Database, username: str, password: str) -> bool:
        """Intenta iniciar sesión y retorna True si es exitoso"""
        password = password.encode("UTF-8")

        resultado = db.query(
            sql="SELECT * FROM USERS WHERE username = :username",
            parameters={"username": username}
        )

        if not resultado or len(resultado) == 0:
            print("Usuario no encontrado")
            return False

        stored_hash = resultado[0][2] 
        stored_hash_bytes = stored_hash.encode("utf-8")

        if bcrypt.checkpw(password, stored_hash_bytes):
            print(f"¡Bienvenido, {username}!")
            return True
        else:
            print("Contraseña incorrecta")
            return False

    @staticmethod
    def register(db: Database, id: int, username: str, password: str):
        """Registra un nuevo usuario"""
        print("Registrando usuario...")
        
        # Verificar si el usuario ya existe
        resultado = db.query(
            sql="SELECT * FROM USERS WHERE username = :username",
            parameters={"username": username}
        )
        
        if resultado and len(resultado) > 0:
            print("El nombre de usuario ya existe")
            return False
            
        # Generar hash de la contraseña
        password = password.encode("UTF-8")
        salt = bcrypt.gensalt(12)
        hash_password = bcrypt.hashpw(password, salt).decode("utf-8")

        usuario = {
            "id": id,
            "username": username,
            "password": hash_password
        }

        try:
            db.query(
                sql="INSERT INTO USERS(id, username, password) VALUES (:id, :username, :password)",
                parameters=usuario
            )
            print("Usuario registrado con éxito")
            return True
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False

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
        except Exception as e:
            print(f"Hubo un error con la solicitud: {e}")
            return 0.0
            
    def get_usd(self, fecha: str = None):
        valor = self.get_indicator("dolar", fecha)
        print(f"El valor del dólar en CLP es: {valor}")
        
    def get_eur(self, fecha: str = None):
        valor = self.get_indicator("euro", fecha)
        print(f"El valor del euro en CLP es: {valor}")
        
    def get_uf(self, fecha: str = None):
        valor = self.get_indicator("uf", fecha)
        print(f"El valor de la UF es: {valor}")
        
    def get_ivp(self, fecha: str = None):
        valor = self.get_indicator("ivp", fecha)
        print(f"El valor del IVP es: {valor}")
        
    def get_ipc(self, fecha: str = None):
        valor = self.get_indicator("ipc", fecha)
        print(f"El valor del IPC es: {valor}")
        
    def get_utm(self, fecha: str = None):
        valor = self.get_indicator("utm", fecha)
        print(f"El valor de la UTM es: {valor}")

# FUNCIONES DE MENÚ
def menu_autenticacion(db: Database):
    """Menú principal de autenticación"""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("""
        =======================================
               SISTEMA DE AUTENTICACIÓN
        =======================================
         1. INICIAR SESIÓN
         2. REGISTRARSE
         3. SALIR
        =======================================
        """)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            os.system("cls" if os.name == "nt" else "clear")
            print("=== INICIAR SESIÓN ===")
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            
            if Auth.login(db, username, password):
                input("\nPresione ENTER para acceder al sistema principal...")
                return True, username  # Retorna éxito y nombre de usuario
            else:
                input("\nPresione ENTER para continuar...")
                
        elif opcion == "2":
            os.system("cls" if os.name == "nt" else "clear")
            print("=== REGISTRAR NUEVO USUARIO ===")
            try:
                id = int(input("ID (número): ").strip())
                username = input("Nombre de usuario: ").strip()
                password = input("Contraseña: ").strip()
                
                if Auth.register(db, id, username, password):
                    input("\nPresione ENTER para continuar...")
                else:
                    input("\nPresione ENTER para volver...")
            except ValueError:
                print("ID debe ser un número entero")
                input("\nPresione ENTER para continuar...")
                
        elif opcion == "3":
            print("Saliendo del sistema...")
            return False, None
            
        else:
            print("Opción inválida")
            input("Presione ENTER para continuar...")

def menu_principal(db: Database, username: str):
    """Menú principal después de autenticación exitosa"""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"""
        =======================================
          SISTEMA INTEGRADO - Usuario: {username}
        =======================================
         1. INDICADORES ECONÓMICOS
         2. CREAR TABLAS (Solo administrador)
         3. CERRAR SESIÓN
        =======================================
        """)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            menu_finanzas()
            
        elif opcion == "2":
            #
            if username.lower() in ["admin", "system"]:
                print("Creando tablas en la base de datos...")
                db.create_all_tables()
                print("Tablas creadas exitosamente")
            else:
                print("No tienes permisos para esta operación")
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "3":
            print(f"Cerrando sesión de {username}...")
            input("Presione ENTER para continuar...")
            break
            
        else:
            print("Opción inválida")
            input("Presione ENTER para continuar...")

def menu_finanzas():
    """Menú de indicadores económicos"""
    finanzas = Finance()
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("""
        =======================================
              INDICADORES ECONÓMICOS
        =======================================
         1. DÓLAR (USD)
         2. EURO (EUR)
         3. UF
         4. IVP
         5. IPC
         6. UTM
         7. CONSULTAR INDICADOR PERSONALIZADO
         8. VOLVER AL MENÚ PRINCIPAL
        =======================================
        """)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\n=== VALOR DEL DÓLAR ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            finanzas.get_usd(fecha)
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "2":
            print("\n=== VALOR DEL EURO ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            finanzas.get_eur(fecha)
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "3":
            print("\n=== VALOR DE LA UF ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            finanzas.get_uf(fecha)
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "4":
            print("\n=== VALOR DEL IVP ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            finanzas.get_ivp(fecha)
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "5":
            print("\n=== VALOR DEL IPC ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            finanzas.get_ipc(fecha)
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "6":
            print("\n=== VALOR DE LA UTM ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            finanzas.get_utm(fecha)
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "7":
            print("\n=== CONSULTA PERSONALIZADA ===")
            indicador = input("Indicador (ej: dolar, euro, uf, ivp, ipc, utm): ").strip().lower()
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            try:
                valor = finanzas.get_indicator(indicador, fecha)
                if valor > 0:
                    print(f"\nValor del {indicador.upper()}: {valor}")
                else:
                    print(f"No se pudo obtener el valor del indicador '{indicador}'")
            except Exception as e:
                print(f"Error: {e}")
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "8":
            break
            
        else:
            print("Opción inválida")
            input("Presione ENTER para continuar...")

def inicializar_sistema():
    """Función principal que inicializa todo el sistema"""
    print("Inicializando sistema...")
    
    
    db = Database(
        username=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )
    
    
    try:
        with db.get_connection() as conn:
            print("✓ Conexión a la base de datos establecida")
    except Exception as e:
        print(f"✗ Error al conectar a la base de datos: {e}")
        print("Asegúrate de que las variables de entorno estén configuradas correctamente")
        input("Presione ENTER para salir...")
        return
    
    a
    while True:
        
        autenticado, username = menu_autenticacion(db)
        
        if not autenticado:
            break
            
        
        menu_principal(db, username)

if __name__ == "__main__":
    inicializar_sistema()