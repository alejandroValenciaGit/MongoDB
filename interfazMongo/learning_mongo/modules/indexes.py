from rich.console import Console  
from rich.table import Table  
from rich.panel import Panel  
from timeit import timeit  
import random 
import string 

console = Console()

def create_sample_data(db):
    """
    Crear datos de ejemplo para pruebas de índices
    Args:
    db: Instancia de base de datos MongoDB
    """
    
    categories = ["Electrónica", "Ropa", "Hogar", "Deportes", "Juguetes"]
    products = []
    
    for i in range(1, 1001):
        product = {
            "name": f"Producto {i}",
            "sku": f"SKU-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}",
            "price": round(random.uniform(10, 1000), 2),
            "category": random.choice(categories),
            "stock": random.randint(0, 500),
            "tags": [f"tag{random.randint(1, 10)}", f"tag{random.randint(1, 10)}"],
            "description": " ".join(["Lorem"] * random.randint(5, 20))
        }
        products.append(product)
    
    db["products"].insert_many(products)
    console.print(f"✅[green]Insertados {len(products)} documentos de ejemplo[/green]")

def run(db):
    """
    Módulo de gestión de índices en MongoDB
    Args:
    db: Instancia de base de datos MongoDB
    """
    console.print(Panel.fit("📊[bold cyan]Gestión de Índices en MongoDB[/bold cyan] 📊"))
    
    if "products" not in db.list_collection_names():
        console.print("\ni️ Creando colección 'products' con datos de ejemplo...")
        create_sample_data(db)
    
    collection = db["products"]
    
    while True:
        table = Table(title="Operaciones con Índices", show_header=True)
        table.add_column("Opción", style="cyan")
        table.add_column("Operación", style="green")
        table.add_column("Descripción", style="white")
        
        table.add_row("1", "Crear índice", "Crear un nuevo índice en la colección")
        table.add_row("2", "Listar índices", "Mostrar todos los índices existentes")
        table.add_row("3", "Eliminar índice", "Remover un índice específico")
        table.add_row("4", "Comparar rendimiento", "Comparar consultas con y sin índice")
        table.add_row("0", "Volver", "Regresar al menú principal")
        
        console.print(table)
        choice = console.input("\n🔹Seleccione una operación (0-4): ")
        
        if choice == "0":
            break
        elif choice == "1":
            console.print("\n[bold]Crear un nuevo índice[/bold]")
            field = console.input("Ingrese el campo a indexar (ej: 'name', 'price'): ")
            index_type = console.input("Tipo de índice (1=ascendente, -1=descendente, 'text'=texto): ")
            
            try:
                if index_type.lower() == "text":
                    collection.create_index([(field, "text")])
                    console.print(f"\n✅[green]Índice de texto creado en el campo '{field}'[/green]")
                else:
                    index_type = int(index_type)
                    collection.create_index([(field, index_type)])
                    console.print(f"\n✅[green]Índice creado en el campo '{field}' ({'ascendente' if index_type == 1 else 'descendente'})[/green]")
            except Exception as e:
                console.print(f"\n❌[red]Error al crear índice: {e}[/red]")
        elif choice == "2":
            console.print("\n[bold]Índices existentes:[/bold]")
            indexes = list(collection.index_information())
            
            if not indexes:
                console.print("i️ No hay índices definidos (solo el índice _id por defecto)")
            else:
                idx_table = Table(title="Índices en colección 'products'", show_header=True)
                idx_table.add_column("Nombre")
                idx_table.add_column("Campos")
                idx_table.add_column("Tipo")
                
                for name, info in collection.index_information().items():
                    fields = ", ".join([f"{k[0]} ({'asc' if k[1] == 1 else 'desc'})" for k in info['key']])
                    idx_type = info.get('weights', 'normal')
                    if idx_type != 'normal':
                        idx_type = 'text'
                    idx_table.add_row(name, fields, idx_type)
                
                console.print(idx_table)
        elif choice == "3":
            console.print("\n[bold]Eliminar un índice[/bold]")
            indexes = list(collection.index_information())
            
            if len(indexes) <= 1:
                console.print("i️ No hay índices adicionales para eliminar")
            else:
                idx_table = Table(title="Índices disponibles para eliminar", show_header=True)
                idx_table.add_column("#", style="cyan")
                idx_table.add_column("Nombre")
                idx_table.add_column("Campos")
                
                for i, name in enumerate(indexes[1:], 1):
                    info = collection.index_information()[name]
                    fields = ", ".join([f"{k[0]} ({'asc' if k[1] == 1 else 'desc'})" for k in info['key']])
                    idx_table.add_row(str(i), name, fields)
                
                console.print(idx_table)
                
                idx_choice = console.input("\nSeleccione el índice a eliminar (número): ")
                try:
                    idx_choice = int(idx_choice)
                    if 1 <= idx_choice < len(indexes):
                        index_name = indexes[idx_choice]
                        collection.drop_index(index_name)
                        console.print(f"\n✅[green]Índice '{index_name}' eliminado correctamente[/green]")
                    else:
                        console.print("\n❌[red]Opción inválida[/red]")
                except Exception as e:
                    console.print(f"\n❌[red]Error al eliminar índice: {e}[/red]")
        else:
            console.print("\n❌[red]Opción inválida. Intente nuevamente.[/red]")
        console.input("\nPresione Enter para continuar...")
        console.clear()