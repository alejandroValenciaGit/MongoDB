from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
import subprocess
import os
from datetime import datetime
import time
import json

console = Console()

def run(db):
    console.print(Panel.fit("⚙️[bold cyan]Administración de MongoDB[/bold cyan] ⚙️"))
    while True:
        table = Table(title="Operaciones de Administración", show_header=True)
        table.add_column("Opción", style="cyan")
        table.add_column("Operación", style="green")
        table.add_column("Descripción", style="white")
        table.add_row("1", "Estadísticas del servidor", "Ver información del servidor MongoDB")
        table.add_row("2", "Gestión de usuarios", "Crear y administrar usuarios")
        table.add_row("3", "Gestión de roles", "Administrar roles y permisos")
        table.add_row("4", "Monitoreo de operaciones", "Ver operaciones en curso")
        table.add_row("5", "Gestión de colecciones", "Administrar colecciones")
        table.add_row("6", "Análisis de rendimiento", "Ver estadísticas de rendimiento")
        table.add_row("0", "Volver", "Regresar al menú principal")
        console.print(table)

        choice = console.input("\n🔹Seleccione una operación (0-6): ")
        if choice == "0":
            break
        elif choice == "1":
            console.print("\n[bold]Estadísticas del servidor:[/bold]")
            try:
                server_info = db.command("serverStatus")
                db_stats = db.command("dbStats")
                info_table = Table(title="Información del Servidor", show_header=False)
                info_table.add_column("Campo")
                info_table.add_column("Valor")
                info_table.add_row("Host", f"{db.client.HOST}:{db.client.PORT}")
                info_table.add_row("Versión MongoDB", server_info["version"])
                info_table.add_row("Motor de almacenamiento", server_info["storageEngine"]["name"])
                info_table.add_row("Tiempo de actividad", f"{server_info['uptime'] / 3600:.2f} horas")
                info_table.add_row("Base de datos actual", db.name)
                info_table.add_row("Tamaño de datos", f"{db_stats['dataSize'] / (1024*1024):.2f} MB")
                info_table.add_row("Almacenamiento usado", f"{db_stats['storageSize'] / (1024*1024):.2f} MB")
                info_table.add_row("Índices", str(db_stats["indexes"]))
                info_table.add_row("Tamaño de índices", f"{db_stats['indexSize'] / (1024*1024):.2f} MB")
                console.print(info_table)
            except Exception as e:
                console.print(f"\n❌[red]Error al obtener estadísticas: {e}[/red]")
        elif choice == "2":
            console.print("\n[bold]Gestión de usuarios[/bold]")
            console.print("1. Listar usuarios\n2. Crear usuario\n3. Modificar roles\n4. Eliminar usuario")
            user_choice = console.input("Seleccione opción (1-4): ")
            admin_db = db.client["admin"]
            if user_choice == "1":
                try:
                    users = list(admin_db.command("usersInfo")["users"])
                    if users:
                        user_table = Table(title="Usuarios del Sistema", show_header=True)
                        user_table.add_column("Usuario")
                        user_table.add_column("Roles")
                        user_table.add_column("Base de datos")
                        for user in users:
                            roles = ", ".join([f"{r['role']}" for r in user["roles"]])
                            dbs = ", ".join(set([r["db"] for r in user["roles"]]))
                            user_table.add_row(user["user"], roles, dbs)
                        console.print(user_table)
                    else:
                        console.print("\ni️ No hay usuarios definidos")
                except Exception as e:
                    console.print(f"\n❌[red]Error al listar usuarios: {e}[/red]")
            elif user_choice == "2":
                try:
                    username = console.input("Nombre de usuario: ")
                    password = console.input("Contraseña: ", password=True)
                    roles_input = console.input("Roles (separados por coma): ")
                    db_name = console.input("Base de datos para los roles: ")
                    roles = [{"role": role.strip(), "db": db_name.strip()} for role in roles_input.split(",")]
                    admin_db.command("createUser", username, pwd=password, roles=roles)
                    console.print("\n✅[green]Usuario creado correctamente[/green]")
                except Exception as e:
                    console.print(f"\n❌[red]Error al crear usuario: {e}[/red]")
        else:
            console.print("\n❌[red]Opción inválida. Intente nuevamente.[/red]")
        console.input("\nPresione Enter para continuar...")
        console.clear()
