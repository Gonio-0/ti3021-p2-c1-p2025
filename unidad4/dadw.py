# app_simple.py - Sin dependencias de colores
import flet as ft
import sqlite3
import hashlib
import secrets
from datetime import datetime

def main(page: ft.Page):
    page.title = "Evaluación POO"
    
    # Inicializar BD
    conn = sqlite3.connect("eval.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user TEXT PRIMARY KEY, pass TEXT, salt TEXT)")
    cursor.execute("""CREATE TABLE IF NOT EXISTS queries 
                    (id INTEGER PRIMARY KEY, user TEXT, indicator TEXT, date TEXT, 
                     value REAL, source TEXT, time TEXT)""")
    conn.commit()
    
    current_user = None
    
    # Pantalla 1: Login
    def show_login():
        page.clean()
        user = ft.TextField(label="Usuario")
        pwd = ft.TextField(label="Contraseña", password=True)
        
        def login_click(e):
            nonlocal current_user
            cursor.execute("SELECT pass, salt FROM users WHERE user=?", (user.value,))
            res = cursor.fetchone()
            if res:
                stored_hash, salt = res
                test_hash = hashlib.sha256((pwd.value + salt).encode()).hexdigest()
                if test_hash == stored_hash:
                    current_user = user.value
                    show_main()
                    return
            page.add(ft.Text("Error: Credenciales incorrectas"))
            page.update()
        
        page.add(
            ft.Column([
                ft.Text("LOGIN", size=30),
                user, pwd,
                ft.ElevatedButton("Entrar", on_click=login_click),
                ft.TextButton("Registrarse", on_click=lambda e: show_register())
            ])
        )
    
    # Pantalla 2: Registro
    def show_register():
        page.clean()
        user = ft.TextField(label="Nuevo usuario")
        pwd = ft.TextField(label="Contraseña", password=True)
        pwd2 = ft.TextField(label="Repetir contraseña", password=True)
        
        def register_click(e):
            if pwd.value != pwd2.value:
                page.add(ft.Text("Error: Contraseñas no coinciden"))
                page.update()
                return
            
            salt = secrets.token_hex(16)
            hash_pass = hashlib.sha256((pwd.value + salt).encode()).hexdigest()
            
            try:
                cursor.execute("INSERT INTO users VALUES (?, ?, ?)", 
                             (user.value, hash_pass, salt))
                conn.commit()
                page.add(ft.Text("✓ Usuario creado"))
                page.update()
                show_login()
            except:
                page.add(ft.Text("Error: Usuario ya existe"))
                page.update()
        
        page.add(
            ft.Column([
                ft.Text("REGISTRO", size=30),
                user, pwd, pwd2,
                ft.ElevatedButton("Crear cuenta", on_click=register_click),
                ft.TextButton("Volver al login", on_click=lambda e: show_login())
            ])
        )
    
    # Pantalla 3: Principal
    def show_main():
        page.clean()
        page.add(
            ft.Column([
                ft.Text(f"Usuario: {current_user}"),
                ft.ElevatedButton("Consultar indicador", on_click=lambda e: show_query()),
                ft.ElevatedButton("Ver historial", on_click=lambda e: show_history()),
                ft.ElevatedButton("Cerrar sesión", on_click=lambda e: [setattr(page, 'clean', lambda: None), show_login()])
            ])
        )
    
    # Pantalla 4: Consulta
    def show_query():
        page.clean()
        indicator = ft.Dropdown(options=[
            ft.dropdown.Option("Dólar"),
            ft.dropdown.Option("Euro"),
            ft.dropdown.Option("UF")
        ], width=200)
        date = ft.TextField(label="Fecha", value="2024-12-25")
        result = ft.Text()
        
        def query_click(e):
            # Simular API
            values = {"Dólar": 850, "Euro": 920, "UF": 36000}
            val = values.get(indicator.value, 0)
            result.value = f"Valor: {val}"
            
            # Guardar en BD
            cursor.execute(
                "INSERT INTO queries (user, indicator, date, value, source, time) VALUES (?, ?, ?, ?, ?, ?)",
                (current_user, indicator.value, date.value, val, "API simulada", datetime.now().isoformat())
            )
            conn.commit()
            page.update()
        
        page.add(
            ft.Column([
                ft.Text("CONSULTAR"),
                indicator, date,
                ft.ElevatedButton("Consultar", on_click=query_click),
                result,
                ft.ElevatedButton("Volver", on_click=lambda e: show_main())
            ])
        )
    
    # Pantalla 5: Historial
    def show_history():
        page.clean()
        cursor.execute(
            "SELECT indicator, date, value, source, time FROM queries WHERE user=? ORDER BY time DESC",
            (current_user,)
        )
        rows = cursor.fetchall()
        
        content = [ft.Text("HISTORIAL")]
        for r in rows:
            content.append(ft.Text(f"{r[0]} - {r[1]}: {r[2]} ({r[3]})"))
        
        content.append(ft.ElevatedButton("Volver", on_click=lambda e: show_main()))
        page.add(ft.Column(content))
    
    show_login()

ft.app(target=main)