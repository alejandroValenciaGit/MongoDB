from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from bson.json_util import dumps
import json
import random
from datetime import datetime

console = Console()

def run(db):
    console.print(Panel.fit("🔢[bold cyan]Agregaciones en MongoDB[/bold cyan] 🔢"))
    if "ventas" not in db.list_collection_names():
        console.print("\ni️ Creando colección 'ventas' con datos de ejemplo...")
        create_sample_sales_data(db)
    collection = db["ventas"]
    
    while True:
        table = Table(title="Operaciones de Agregación", show_header=True)
        table.add_column("Opción", style="cyan")
        table.add_column("Operación", style="green")
        table.add_column("Descripción", style="white")
        table.add_row("1", "Agregación básica", "Ejemplo: Conteo y suma de ventas")
        table.add_row("2", "Agrupación por campo", "Agrupar por categoría/producto")
        table.add_row("3", "Filtros en pipelines", "Filtrar antes de agrupar")
        table.add_row("4", "Operadores avanzados", "Uso de $lookup, $unwind")
        table.add_row("5", "Pipeline personalizado", "Escribir tu propio pipeline")
        table.add_row("6", "Análisis temporal", "Agregaciones por fecha")
        table.add_row("7", "Estadísticas avanzadas", "Métricas y análisis detallado")
        table.add_row("0", "Volver", "Regresar al menú principal")
        console.print(table)
        
        choice = console.input("\n🔹Seleccione una operación (0-7): ")
        
        if choice == "0":
            break
        elif choice == "1":
            console.print("\n[bold]Agregación Básica:[/bold] Conteo y total de ventas")
            pipeline = [
                {"$group": {
                    "_id": None,
                    "total_ventas": {"$sum": "$monto"},
                    "cantidad_ventas": {"$sum": 1},
                    "promedio_venta": {"$avg": "$monto"},
                    "venta_minima": {"$min": "$monto"},
                    "venta_maxima": {"$max": "$monto"}
                }}
            ]
            print_aggregation(collection, pipeline)
        elif choice == "2":
            console.print("\n[bold]Agrupación por Producto:[/bold] Análisis detallado de ventas")
            pipeline = [
                {"$group": {
                    "_id": "$producto",
                    "total_ventas": {"$sum": "$monto"},
                    "cantidad_ventas": {"$sum": 1},
                    "promedio_venta": {"$avg": "$monto"},
                    "venta_minima": {"$min": "$monto"},
                    "venta_maxima": {"$max": "$monto"}
                }},
                {"$project": {
                    "producto": "$_id",
                    "total_ventas": {"$round": ["$total_ventas", 2]},
                    "cantidad_ventas": 1,
                    "promedio_venta": {"$round": ["$promedio_venta", 2]},
                    "venta_minima": {"$round": ["$venta_minima", 2]},
                    "venta_maxima": {"$round": ["$venta_maxima", 2]}
                }},
                {"$sort": {"total_ventas": -1}}
            ]
            print_aggregation(collection, pipeline)

def print_aggregation(collection, pipeline):
    console.print("\n[bold]Pipeline ejecutado:[/bold]")
    console.print(dumps(pipeline, indent=2))
    try:
        results = list(collection.aggregate(pipeline))
        if not results:
            console.print("\ni️ No se encontraron resultados")
            return
        table = Table(title="Resultados de Agregación", show_header=True)
        for key in results[0].keys():
            if key != "_id":
                table.add_column(str(key))
        for doc in results:
            row_data = [str(doc[key]) for key in doc.keys() if key != "_id"]
            table.add_row(*row_data)
        console.print(table)
        if len(results) > 1:
            console.print(f"\nTotal de resultados: {len(results)}")
    except Exception as e:
        console.print(f"\n❌[red]Error en agregación: {e}[/red]")

def create_sample_sales_data(db):
    productos = ["Laptop", "Smartphone", "Camisa", "Zapatos", "Libro"]
    vendedores = [f"Vendedor-{i}" for i in range(1, 6)]
    metodos_pago = ["Tarjeta", "Efectivo", "Transferencia", "Crypto", "PayPal"]
    ventas = []
    for _ in range(1000):
        fecha = datetime(2023, random.randint(1, 12), random.randint(1, 28))
        venta = {
            "producto": random.choice(productos),
            "monto": round(random.uniform(10, 1000), 2),
            "fecha": fecha.strftime("%Y-%m-%d"),
            "vendedor": random.choice(vendedores),
            "metodo_pago": random.choice(metodos_pago),
            "cantidad": random.randint(1, 5),
            "descuento": random.choice([0, 5, 10, 15, 20])
        }
        ventas.append(venta)
    db["ventas"].insert_many(ventas)
    console.print(f"✅[green]Insertadas {len(ventas)} ventas de ejemplo[/green]")
