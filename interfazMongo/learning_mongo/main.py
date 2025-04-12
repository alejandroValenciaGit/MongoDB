import os
from dotenv import load_dotenv
from pymongo import MongoClient
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from modules import validation
from modules import transactions
from modules import indexes

# → ➡️✔️​❌​❔​🔎​♻️​☠️​📥​📚​👨‍🦼​
console = Console()

def insert_document(collection):
    console.print("\n[bold cyan]📥​ Insertar documento[/bold cyan]")
    nombre = console.input("Nombre: ")
    correo = console.input("Correo: ")
    edad = console.input("Edad: ")
    
    documento = {"nombre": nombre, "correo": correo, "edad": int(edad)}
    resultado = collection.insert_one(documento)
    console.print(f"[green]✔️ Documento insertado con ID: [/green] {resultado.inserted_id}")

def find_document(collection):
    console.print("\n [bold cyan]❔​ Buscar documentos[/bold cyan]")
    documentos = collection.find()
    
    tabla = Table(title = "Usuarios encontrados", show_lines = True)
    tabla.add_column("ID", style = "magenta")
    tabla.add_column("Nombre", style = "cyan")
    tabla.add_column("Correo", style = "green")
    tabla.add_column("Edad", style = "yellow")
    
    for doc in documentos:
        tabla.add_row(
            str(doc.get("_id")),
            doc.get("nombre", "N/A"),
            doc.get("correo", "N/A"),
            str(doc.get("edad", "N/A"))
        )
    console.print(tabla)

def update_document(collection):
    console.print("\n [bold cyan]♻️​ Actualizar documento[/bold cyan]")
    correo = console.input("Correo del usuario a actualizar: ")
    nuevo_nombre = console.input("Nuevo nombre: ")
    nueva_edad = console.input("Nueva edad: ")
    
    resultado = collection.update_one(
        {"correo": correo},
        {"$set": {"nombre": nuevo_nombre, "edad": int(nueva_edad)}}
    )
    
    if resultado.modified_count > 0:
        console.print("[green]✔️ Documento actualizado correctamente[/green]")
    else:
        console.print("[yellow]❌ No se encontro ningun documento con ese correo[/yellow]")

def delete_document(collection):
    console.print("\n [bold cyan]☠️ Eliminar documento[/bold cyan]")
    correo = console.input("Correo del usuario a eliminar: ")
    
    resultado = collection.delete_one({"correo": correo})
    
    if resultado.deleted_count > 0:
        console.print("[red]​​☠️ Documento eliminado correctamente[/red]")
    else:
        console.print("[yellow]​❌​ No se encontro ningun documento con ese correo[/yellow]")

def show_menu():
    console.print(Panel.fit("[bold cyan]📚​ Aprende MongoDB con python 📚​[/bold cyan]"))
    
    menu = Table(title = "Modulos disponibles", show_header = True, header_style = "bold magenta")
    menu.add_column("Opcion", style = "cyan")
    menu.add_column("Operacion", style = "green")
    menu.add_column("Descripcion", style = "white")
    
    menu.add_row("1", "Insertar documento", "Aprende a insertar documentos a MongoDB")
    menu.add_row("2", "Buscar documentos", "Realizar consultas en la base de datos")
    menu.add_row("3", "Actualizar documento", "Modificar documentos existentes")
    menu.add_row("4", "Eliminar documento", "Eliminar documentos de la coleccion")
    menu.add_row("5", "Validacion de esquemas", "Gestionar reglas de validacion")
    menu.add_row("6", "Transacciones", "Operaciones transaccionales ACID")
    menu.add_row("7", "Indices", "Gestion y analisi de indices")
    menu.add_row("0", "Salir", "Terminar el programa")
    
    console.print(menu)

def main():
    load_dotenv()
    
    try:
        client = MongoClient("mongodb://localhost:27017")
        client.admin.command("ping")
        
        db = client[os.getenv("DB_NAME", "tutorial_db")]
        collection = db["usuarios"]
        
        console.print("[green]✔️ Conexion exitosa a MongoDB[/green]")
        
        operations = {
            "1": lambda: insert_document(collection),
            "2": lambda: find_document(collection),
            "3": lambda: update_document(collection),
            "4": lambda: delete_document(collection),
            "5": lambda: validation.run(db),
            "6": lambda: transactions.run(db),
            "7": lambda: indexes.run(db)
        }
        
        while True:
            show_menu()
            choice = console.input('\n[cyan]➡️  Seleccione una opcion (0/7)[/cyan]')
            
            if choice == "0":
                console.print("\n[yellow] 👋​ Hasta Luego 👋​ [/yellow]")
                break
            
            if choice in operations:
                operations[choice]()
            else:
                console.print(f"[red]👨‍🦼​ Opcion invalida intente nuevamente[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error de conexion {e}[/red]")

if __name__ == "__main__":
    main()