from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from bson.objectid import ObjectId

console = Console()

def try_eval(value):
    try:
        return eval(value)
    except:
        return value

def print_documents(docs):
    if not docs:
        console.print("\ni️ No se encontraron documentos")
        return
    
    table = Table(title="Documentos Encontrados", show_header=True)
    for key in docs[0].keys():
        table.add_column(str(key))
    
    for doc in docs:
        row = []
        for val in doc.values():
            if isinstance(val, ObjectId):
                row.append(str(val))
            else:
                row.append(str(val))
        table.add_row(*row)
    
    console.print(table)

def run(db):
    console.print(Panel.fit("📝[bold cyan]Operaciones CRUD en MongoDB[/bold cyan] 📝"))
    
    collections = db.list_collection_names()
    if not collections:
        console.print("\ni️ No hay colecciones en esta base de datos. Creando una nueva...")
        collection_name = "ejemplo_crud"
        db.create_collection(collection_name)
    else:
        collection_name = console.input(f"\nIngrese el nombre de la colección ({', '.join(collections)}): ")
    
    collection = db[collection_name]
    
    while True:
        table = Table(title="Operaciones CRUD", show_header=True)
        table.add_column("Opción", style="cyan")
        table.add_column("Operación", style="green")
        table.add_column("Descripción", style="white")
        
        table.add_row("1", "Insertar", "Agregar nuevos documentos")
        table.add_row("2", "Buscar", "Consultar documentos")
        table.add_row("3", "Actualizar", "Modificar documentos")
        table.add_row("4", "Eliminar", "Borrar documentos")
        table.add_row("5", "Conteo", "Contar documentos")
        table.add_row("0", "Volver", "Regresar al menú principal")
        
        console.print(table)
        choice = console.input("\n🔹Seleccione una operación CRUD (0-5): ")
        
        if choice == "0":
            break
        elif choice == "1":
            console.print("\n[bold]Insertar documentos[/bold]")
            console.print("1. Insertar uno\n2. Insertar varios")
            insert_choice = console.input("Seleccione opción (1-2): ")
            
            if insert_choice == "1":
                doc = {}
                while True:
                    key = console.input("Ingrese clave (o dejar vacío para terminar): ")
                    if not key:
                        break
                    value = console.input(f"Ingrese valor para '{key}': ")
                    doc[key] = try_eval(value)
                
                if doc:
                    result = collection.insert_one(doc)
                    console.print(f"\n✅[green]Documento insertado con ID: {result.inserted_id}[/green]")
                else:
                    console.print("\n❌[red]No se proporcionaron datos para insertar[/red]")
            
            elif insert_choice == "2":
                docs = []
                console.print("\nIngrese documentos (deje vacío para terminar):")
                
                while True:
                    doc = {}
                    console.print(f"\nDocumento #{len(docs) + 1}:")
                    while True:
                        key = console.input("Ingrese clave (o dejar vacío para terminar documento): ")
                        if not key:
                            break
                        value = console.input(f"Ingrese valor para '{key}': ")
                        doc[key] = try_eval(value)
                    
                    if doc:
                        docs.append(doc)
                    else:
                        break
                
                if docs:
                    result = collection.insert_many(docs)
                    console.print(f"\n✅[green]Insertados {len(result.inserted_ids)} documentos[/green]")
                    console.print(f"IDs: {result.inserted_ids}")
                else:
                    console.print("\n❌[red]No se proporcionaron documentos para insertar[/red]")
        
        elif choice == "2":
            console.print("\n[bold]Buscar documentos[/bold]")
            console.print("1. Buscar todos\n2. Buscar con filtro\n3. Buscar uno")
            find_choice = console.input("Seleccione opción (1-3): ")
            
            if find_choice == "1":
                docs = list(collection.find())
                print_documents(docs)
            elif find_choice == "2":
                try:
                    query = console.input("Ingrese filtro (ej: {'nombre': 'Juan'}): ")
                    query = eval(query) if query else {}
                    docs = list(collection.find(query))
                    print_documents(docs)
                except Exception as e:
                    console.print(f"\n❌[red]Error en la consulta: {e}[/red]")
            elif find_choice == "3":
                try:
                    query = console.input("Ingrese filtro (ej: {'_id': ObjectId('...')}): ")
                    query = eval(query) if query else {}
                    doc = collection.find_one(query)
                    if doc:
                        print_documents([doc])
                    else:
                        console.print("\ni️ No se encontraron documentos")
                except Exception as e:
                    console.print(f"\n❌[red]Error en la consulta: {e}[/red]")
        
        console.input("\nPresione Enter para continuar...")
        console.clear()
