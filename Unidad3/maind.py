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
                "CREATE TABLE usuarios("
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
        print("Tablas creadas exitosamente")

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
            sql= "SELECT * FROM usuarios WHERE username = :username",
            parameters={"username":username}
        )

        if len(resultado) == 0:
            return print("No hay coincidencias")

        stored_hash = resultado[0][2]          # cadena desde DB
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
            sql= "INSERT INTO usuarios(id,username,password) VALUES (:id, :username, :password)",
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
        # Obtener el próximo ID
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
        
        print("✓ Consulta registrada en la base de datos")
        return True
        
    except Exception as e:
        print(f"⚠️ No se pudo registrar la consulta: {e}")
        return False

def ver_consultas(db: Database):
    """Muestra todas las consultas registradas"""
    os.system("cls" if os.name == "nt" else "clear")
    print("""
    =======================================
          CONSULTAS REGISTRADAS
    =======================================
    """)
    
    try:
        consultas = db.query("SELECT * FROM CONSULTAS ORDER BY fecha_consulta DESC")
        
        if not consultas:
            print("No hay consultas registradas")
        else:
            print(f"Total de consultas: {len(consultas)}")
            print("-" * 80)
            
            for consulta in consultas:
                id_consulta, nombre, fecha_ind, valor, fecha_cons, usuario = consulta
                
                # Formatear fechas
                fecha_ind_str = fecha_ind.strftime("%d-%m-%Y") if fecha_ind else "N/A"
                fecha_cons_str = fecha_cons.strftime("%d-%m-%Y %H:%M") if fecha_cons else "N/A"
                
                print(f"ID: {id_consulta} | Usuario: {usuario}")
                print(f"  Indicador: {nombre}")
                print(f"  Fecha consultada: {fecha_ind_str}")
                print(f"  Valor: ${valor:,.2f}")
                print(f"  Fecha de consulta: {fecha_cons_str}")
                print("-" * 80)
                
    except Exception as e:
        print(f"Error al obtener consultas: {e}")
    
    input("\nPresione ENTER para continuar...")

def mostrar_menu_principal():
    """Muestra el menú principal"""
    print("\n" + "="*50)
    print("SISTEMA DE INDICADORES ECONÓMICOS")
    print("="*50)
    print("1. Crear tablas (USUARIOS y CONSULTAS)")
    print("2. Registrar usuario")
    print("3. Iniciar sesión")
    print("4. Consultar indicadores")
    print("5. Ver consultas registradas")
    print("6. Salir")
    print("="*50)

def mostrar_menu_consultas():
    """Muestra el menú de consultas"""
    print("\n" + "="*40)
    print("CONSULTAR INDICADORES ECONÓMICOS")
    print("="*40)
    print("1. Dólar (USD)")
    print("2. Euro (EUR)")
    print("3. Unidad de Fomento (UF)")
    print("4. Índice de Valor Promedio (IVP)")
    print("5. Índice de Precio al Consumidor (IPC)")
    print("6. Unidad Tributaria Mensual (UTM)")
    print("7. Volver al menú principal")
    print("="*40)

def menu_consultas_indices(db: Database, finanzas: Finance, usuario_actual: str):
    """Maneja el menú de consultas de indicadores"""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        mostrar_menu_consultas()
        
        opcion = input("\nSeleccione una opción (1-7): ").strip()
        
        if opcion == "1":
            print("\n" + "="*40)
            print("CONSULTAR DÓLAR (USD)")
            print("="*40)
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            valor = finanzas.get_usd(fecha)
            
            # Registrar consulta
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
            print("\n" + "="*40)
            print("CONSULTAR EURO (EUR)")
            print("="*40)
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
            print("\n" + "="*40)
            print("CONSULTAR UNIDAD DE FOMENTO (UF)")
            print("="*40)
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
            print("\n" + "="*40)
            print("CONSULTAR ÍNDICE DE VALOR PROMEDIO (IVP)")
            print("="*40)
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
            print("\n" + "="*40)
            print("CONSULTAR ÍNDICE DE PRECIO AL CONSUMIDOR (IPC)")
            print("="*40)
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
            print("\n" + "="*40)
            print("CONSULTAR UNIDAD TRIBUTARIA MENSUAL (UTM)")
            print("="*40)
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
            break
            
        else:
            print("Opción inválida. Intente nuevamente.")
            input("\nPresione ENTER para continuar...")

def menu_principal():
    """Función principal con menú interactivo"""
    # Crear conexión a la base de datos
    db = Database(
        username=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )
    
    finanzas = Finance()
    usuario_actual = None
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        
        if usuario_actual:
            print(f"\nUsuario actual: {usuario_actual}")
        
        mostrar_menu_principal()
        opcion = input("\nSeleccione una opción (1-6): ").strip()
        
        if opcion == "1":
            print("\nCreando tablas USUARIOS y CONSULTAS...")
            db.create_all_tables()
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "2":
            print("\n" + "="*40)
            print("REGISTRAR NUEVO USUARIO")
            print("="*40)
            try:
                id_usuario = int(input("ID del usuario: "))
                username = input("Nombre de usuario: ")
                password = input("Contraseña: ")
                Auth.register(db, id_usuario, username, password)
            except ValueError:
                print("Error: El ID debe ser un número entero")
            except Exception as e:
                print(f"Error: {e}")
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "3":
            print("\n" + "="*40)
            print("INICIAR SESIÓN")
            print("="*40)
            username = input("Usuario: ")
            password = input("Contraseña: ")
            
            # Verificar credenciales
            try:
                resultado = db.query(
                    sql="SELECT * FROM USUARIOS WHERE username = :username",
                    parameters={"username": username}
                )
                
                if len(resultado) == 0:
                    print("Usuario no encontrado")
                else:
                    stored_hash = resultado[0][2]
                    stored_hash_bytes = stored_hash.encode("utf-8")
                    
                    if bcrypt.checkpw(password.encode("UTF-8"), stored_hash_bytes):
                        usuario_actual = username
                        print(f"¡Bienvenido {usuario_actual}!")
                    else:
                        print("Contraseña incorrecta")
                        
            except Exception as e:
                print(f"Error: {e}")
                
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "4":
            if usuario_actual:
                menu_consultas_indices(db, finanzas, usuario_actual)
            else:
                print("\nDebe iniciar sesión primero para consultar indicadores.")
                input("\nPresione ENTER para continuar...")
                
        elif opcion == "5":
            ver_consultas(db)
            
        elif opcion == "6":
            print("\nSaliendo del sistema...")
            print("¡Hasta luego!")
            break
            
        else:
            print("\nOpción inválida. Por favor seleccione 1-6.")
            input("\nPresione ENTER para continuar...")

if __name__ == "__main__":
    menu_principal()