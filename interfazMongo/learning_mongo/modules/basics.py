from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def run(db):
    console.print(Panel.fit("📌[bold cyan]Conceptos Básicos de MongoDB[/bold cyan] 📌"))
    
    while True:
        table = Table(title="Operaciones Básicas", show_header=True)
        table.add_column("Opción", style="cyan")
        table.add_column("Comando", style="green")
        table.add_column("Descripción", style="white")
        
        table.add_row("1", "db.help()", "Mostrar ayuda de comandos de base de datos")
        table.add_row("2", "db.stats()", "Mostrar estadísticas de la BD")
        table.add_row("3", "show dbs", "Listar todas las bases de datos")
        table.add_row("4", "use <db>", "Cambiar a una base de datos")
        table.add_row("5", "db.dropDatabase()", "Eliminar la base de datos actual")
        table.add_row("6", "db.createCollection()", "Crear una nueva colección")
        table.add_row("7", "show collections", "Listar colecciones en la BD actual")
        table.add_row("8", "db.<col>.drop()", "Eliminar una colección")
        table.add_row("0", "Volver", "Regresar al menú principal")
        
        console.print(table)
        choice = console.input("\n🔹Seleccione una operación para ejecutar (0-8): ")
        
        if choice == "0":
            break
        elif choice == "1":
            console.print("\n[bold]Ejemplo de db.help():[/bold]")
            console.print("""
            Este comando muestra todos los métodos disponibles para manipular la base de datos.
            [yellow]Uso:[/yellow]
            > db.help()
            """)
        elif choice == "2":
            console.print("\n[bold]Ejemplo de db.stats():[/bold]")
            try:
                stats = db.command("dbstats")
                result_table = Table(title="Estadísticas de la Base de Datos")
                result_table.add_column("Métrica", style="cyan")
                result_table.add_column("Valor", style="green")
                
                metrics = {
                    "db": "Nombre de la base de datos",
                    "collections": "Número total de colecciones",
                    "views": "Número de vistas",
                    "objects": "Número total de documentos",
                    "avgObjSize": "Tamaño promedio de documentos (bytes)",
                    "dataSize": "Tamaño total de datos (bytes)",
                    "storageSize": "Tamaño en disco (bytes)",
                    "indexes": "Número total de índices",
                    "indexSize": "Tamaño total de índices (bytes)",
                    "totalSize": "Tamaño total (datos + índices)",
                    "scaleFactor": "Factor de escala para métricas",
                }
                
                for key, desc in metrics.items():
                    if key in stats:
                        value = stats[key]
                        if isinstance(value, (int, float)) and key.endswith("Size"):
                            value = format_bytes(value)
                        result_table.add_row(f"{key} ({desc})", str(value))
                
                console.print(result_table)
            except Exception as e:
                console.print(f"\n❌[red]Error al obtener estadísticas: {e}[/red]")
        elif choice == "3":
            console.print("\n[bold]Ejemplo de show dbs:[/bold]")
            try:
                dbs = db.client.list_database_names()
                db_table = Table(title="Bases de Datos Disponibles")
                db_table.add_column("Nombre", style="cyan")
                db_table.add_column("Tamaño", style="green")
                
                for db_name in dbs:
                    size = db.client[db_name].command("dbstats")["dataSize"]
                    db_table.add_row(db_name, format_bytes(size))
                
                console.print(db_table)
            except Exception as e:
                console.print(f"\n❌[red]Error al listar bases de datos: {e}[/red]")
        
        console.input("\nPresione Enter para continuar...")
        console.clear()

def format_bytes(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"
