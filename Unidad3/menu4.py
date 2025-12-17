import bcrypt
import requests
import oracledb
import os
from dotenv import load_dotenv
from typing import Optional, Tuple
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
        """Crea todas las tablas necesarias"""
        tables = [
            # Tabla de usuarios
            """
            CREATE TABLE USERS(
                id INTEGER PRIMARY KEY,
                username VARCHAR(32) UNIQUE,
                password VARCHAR(128)
            )
            """,
            # Tabla de registros de consultas
            """
            CREATE TABLE CONSULTAS_INDICADORES(
                id INTEGER PRIMARY KEY,
                nombre_indicador VARCHAR(50),
                fecha_indicador DATE,
                valor_indicador NUMBER(15,2),
                fecha_consulta TIMESTAMP,
                usuario_consulta VARCHAR(50),
                sitio_proveedor VARCHAR(100)
            )
            """
        ]

        for table in tables:
            self.query(table)
        print("✓ Tablas creadas exitosamente")

    def query(self, sql: str, parameters: Optional[dict] = None):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    ejecucion = cur.execute(sql, parameters)
                    if sql.strip().upper().startswith("SELECT"):
                        resultado = []
                        for fila in ejecucion:
                            resultado.append(fila)
                        return resultado
                conn.commit()
        except oracledb.DatabaseError as error:
            print(f"Error en la consulta: {error}")

class Auth:
    @staticmethod
    def login(db: Database, username: str, password: str) -> Tuple[bool, Optional[int]]:
        """Intenta iniciar sesión y retorna (éxito, user_id)"""
        password = password.encode("UTF-8")

        resultado = db.query(
            sql="SELECT id, password FROM USERS WHERE username = :username",
            parameters={"username": username}
        )

        if not resultado or len(resultado) == 0:
            print("Usuario no encontrado")
            return False, None

        user_id = resultado[0][0]
        stored_hash = resultado[0][1]
        stored_hash_bytes = stored_hash.encode("utf-8")

        if bcrypt.checkpw(password, stored_hash_bytes):
            print(f"¡Bienvenido, {username}!")
            return True, user_id
        else:
            print("Contraseña incorrecta")
            return False, None

class Finance:
    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url
        self.sitio_proveedor = "mindicador.cl"
        
    # MANTENGO TU FUNCIÓN GET_INDICATOR EXACTAMENTE COMO ESTÁ
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
        print(f"El valor del dólar en CLP es: {valor}")
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

# FUNCIONES PARA REGISTRAR CONSULTAS
def registrar_consulta(db: Database, usuario: str, indicador: str, fecha: str, valor: float):
    """Registra una consulta en la base de datos"""
    try:
        # Crear diccionario con los datos
        consulta = {
            "nombre_indicador": indicador,
            "fecha_indicador": fecha,
            "valor_indicador": valor,
            "fecha_consulta": datetime.datetime.now(),
            "usuario_consulta": usuario,
            "sitio_proveedor": "mindicador.cl"
        }
        
        # Insertar en la base de datos
        db.query(
            sql="""
            INSERT INTO CONSULTAS_INDICADORES 
            (id, nombre_indicador, fecha_indicador, valor_indicador, 
             fecha_consulta, usuario_consulta, sitio_proveedor)
            VALUES ((SELECT NVL(MAX(id), 0) + 1 FROM CONSULTAS_INDICADORES), 
                    :nombre_indicador, TO_DATE(:fecha_indicador, 'DD-MM-YYYY'), 
                    :valor_indicador, :fecha_consulta, :usuario_consulta, :sitio_proveedor)
            """,
            parameters=consulta
        )
        
        print("✓ Consulta registrada en la base de datos")
        return True
        
    except Exception as e:
        print(f"⚠️ No se pudo registrar la consulta: {e}")
        return False

def ver_historial_consultas(db: Database, usuario: str):
    """Muestra el historial de consultas del usuario"""
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""
    =======================================
          HISTORIAL DE CONSULTAS - {usuario}
    =======================================
    """)
    
    try:
        # Obtener consultas del usuario
        consultas = db.query(
            sql="""
            SELECT nombre_indicador, fecha_indicador, valor_indicador, 
                   fecha_consulta, sitio_proveedor
            FROM CONSULTAS_INDICADORES 
            WHERE usuario_consulta = :usuario
            ORDER BY fecha_consulta DESC
            """,
            parameters={"usuario": usuario}
        )
        
        if not consultas:
            print("No hay consultas registradas")
        else:
            print(f"📋 Total de consultas: {len(consultas)}")
            print("-" * 70)
            print(f"{'Indicador':<15} {'Fecha':<12} {'Valor':<15} {'Consulta':<20} {'Proveedor':<15}")
            print("-" * 70)
            
            for consulta in consultas:
                nombre, fecha_ind, valor, fecha_cons, proveedor = consulta
                
                # Formatear fechas
                fecha_ind_str = fecha_ind.strftime("%d-%m-%Y") if fecha_ind else "N/A"
                fecha_cons_str = fecha_cons.strftime("%d-%m-%Y %H:%M") if fecha_cons else "N/A"
                
                # Formatear valor
                if "IPC" in nombre.upper():
                    valor_str = f"{valor}%"
                else:
                    valor_str = f"${valor:,.2f}"
                
                print(f"{nombre:<15} {fecha_ind_str:<12} {valor_str:<15} {fecha_cons_str:<20} {proveedor:<15}")
            
            print("-" * 70)
            
    except Exception as e:
        print(f"Error al obtener historial: {e}")
    
    input("\nPresione ENTER para continuar...")

# FUNCIONES DE MENÚ
def menu_autenticacion(db: Database):
    """Menú de autenticación"""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("""
        =======================================
               SISTEMA DE INDICADORES ECONÓMICOS
        =======================================
         1. INICIAR SESIÓN
         2. SALIR
        =======================================
        """)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            os.system("cls" if os.name == "nt" else "clear")
            print("=== INICIAR SESIÓN ===")
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()
            
            autenticado, user_id = Auth.login(db, username, password)
            if autenticado:
                input("\nPresione ENTER para acceder al sistema...")
                return True, username
            else:
                input("\nPresione ENTER para continuar...")
                
        elif opcion == "2":
            print("Saliendo del sistema...")
            return False, None
            
        else:
            print("Opción inválida")
            input("Presione ENTER para continuar...")

def menu_principal(db: Database, username: str):
    """Menú principal después de autenticación"""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"""
        =======================================
          SISTEMA DE INDICADORES - {username}
        =======================================
         1. INDICADORES ECONÓMICOS
         2. VER MI HISTORIAL DE CONSULTAS
         3. CREAR TABLAS (Admin)
         4. CERRAR SESIÓN
        =======================================
        """)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            menu_finanzas(db, username)
            
        elif opcion == "2":
            ver_historial_consultas(db, username)
            
        elif opcion == "3":
            if username.lower() in ["admin", "system"]:
                print("Creando tablas en la base de datos...")
                db.create_all_tables()
            else:
                print("No tienes permisos para esta operación")
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "4":
            print(f"Cerrando sesión de {username}...")
            input("Presione ENTER para continuar...")
            break
            
        else:
            print("Opción inválida")
            input("Presione ENTER para continuar...")

def menu_finanzas(db: Database, username: str):
    """Menú de indicadores económicos con registro automático"""
    finanzas = Finance()
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"""
        =======================================
              INDICADORES ECONÓMICOS - {username}
        =======================================
         1. DÓLAR (USD)
         2. EURO (EUR)
         3. UF
         4. IVP
         5. IPC
         6. UTM
         7. VOLVER AL MENÚ PRINCIPAL
        =======================================
        """)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\n=== CONSULTAR DÓLAR ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            
            # Obtener valor
            valor = finanzas.get_usd(fecha)
            
            # Si hay fecha específica, usarla, sino usar hoy
            if fecha:
                fecha_consulta = fecha
            else:
                dd = datetime.datetime.now().day
                mm = datetime.datetime.now().month
                yyyy = datetime.datetime.now().year
                fecha_consulta = f"{dd}-{mm}-{yyyy}"
            
            # Registrar consulta si se obtuvo un valor
            if valor > 0:
                registrar_consulta(db, username, "Dólar", fecha_consulta, valor)
            
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "2":
            print("\n=== CONSULTAR EURO ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            
            valor = finanzas.get_eur(fecha)
            
            if fecha:
                fecha_consulta = fecha
            else:
                dd = datetime.datetime.now().day
                mm = datetime.datetime.now().month
                yyyy = datetime.datetime.now().year
                fecha_consulta = f"{dd}-{mm}-{yyyy}"
            
            if valor > 0:
                registrar_consulta(db, username, "Euro", fecha_consulta, valor)
            
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "3":
            print("\n=== CONSULTAR UF ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            
            valor = finanzas.get_uf(fecha)
            
            if fecha:
                fecha_consulta = fecha
            else:
                dd = datetime.datetime.now().day
                mm = datetime.datetime.now().month
                yyyy = datetime.datetime.now().year
                fecha_consulta = f"{dd}-{mm}-{yyyy}"
            
            if valor > 0:
                registrar_consulta(db, username, "UF", fecha_consulta, valor)
            
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "4":
            print("\n=== CONSULTAR IVP ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            
            valor = finanzas.get_ivp(fecha)
            
            if fecha:
                fecha_consulta = fecha
            else:
                dd = datetime.datetime.now().day
                mm = datetime.datetime.now().month
                yyyy = datetime.datetime.now().year
                fecha_consulta = f"{dd}-{mm}-{yyyy}"
            
            if valor > 0:
                registrar_consulta(db, username, "IVP", fecha_consulta, valor)
            
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "5":
            print("\n=== CONSULTAR IPC ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            
            valor = finanzas.get_ipc(fecha)
            
            if fecha:
                fecha_consulta = fecha
            else:
                dd = datetime.datetime.now().day
                mm = datetime.datetime.now().month
                yyyy = datetime.datetime.now().year
                fecha_consulta = f"{dd}-{mm}-{yyyy}"
            
            if valor > 0:
                registrar_consulta(db, username, "IPC", fecha_consulta, valor)
            
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "6":
            print("\n=== CONSULTAR UTM ===")
            fecha = input("Fecha (dd-mm-yyyy) o ENTER para hoy: ").strip() or None
            
            valor = finanzas.get_utm(fecha)
            
            if fecha:
                fecha_consulta = fecha
            else:
                dd = datetime.datetime.now().day
                mm = datetime.datetime.now().month
                yyyy = datetime.datetime.now().year
                fecha_consulta = f"{dd}-{mm}-{yyyy}"
            
            if valor > 0:
                registrar_consulta(db, username, "UTM", fecha_consulta, valor)
            
            input("\nPresione ENTER para continuar...")
            
        elif opcion == "7":
            break
            
        else:
            print("Opción inválida")
            input("Presione ENTER para continuar...")

def inicializar_sistema():
    """Función principal que inicializa todo el sistema"""
    print("Inicializando Sistema de Indicadores Económicos...")
    
    # Crear conexión a la base de datos
    db = Database(
        username=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )
    
    # Verificar conexión
    try:
        with db.get_connection() as conn:
            print("✓ Conexión a la base de datos establecida")
    except Exception as e:
        print(f"✗ Error al conectar a la base de datos: {e}")
        input("Presione ENTER para salir...")
        return
    
    # Ciclo principal del sistema
    while True:
        # Menú de autenticación
        autenticado, username = menu_autenticacion(db)
        
        if not autenticado:
            break
            
        # Menú principal (solo si se autenticó correctamente)
        menu_principal(db, username)

if __name__ == "__main__":
    inicializar_sistema()