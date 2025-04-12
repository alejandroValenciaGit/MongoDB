from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from bson.son import SON

console = Console()

def run(db):
    console.print(Panel.fit("🔍[bold cyan]Validación de Esquemas en MongoDB[/bold cyan]🔍"))
    
    collections = db.list_collection_names()
    if not collections:
        collection_name = "validated_users"
        db.create_collection(collection_name)
    else:
        collection_name = console.input(f"\nIngrese el nombre de la colección ({', '.join(collections)}): ")
    
    collection = db[collection_name]
    
    while True:
        table = Table(title="Operaciones de Validación", show_header=True)
        table.add_column("Opción", style="cyan")
        table.add_column("Operación", style="green")
        table.add_column("Descripción", style="white")
        
        table.add_row("1", "Mostrar reglas actuales", "Ver las reglas de validación existentes")
        table.add_row("2", "Agregar validación simple", "Añadir validación básica a la colección")
        table.add_row("3", "Agregar validación JSON Schema", "Añadir validación con esquema JSON")
        table.add_row("4", "Eliminar validación", "Remover todas las reglas de validación")
        table.add_row("5", "Probar validación", "Insertar documentos para probar las reglas")
        table.add_row("0", "Volver", "Regresar al menú principal")
        
        console.print(table)
        choice = console.input("\n🔹Seleccione una operación (0-5): ")
        
        if choice == "0":
            break
        elif choice == "1":
            console.print("\n[bold]Reglas de validación actuales:[/bold]")
            try:
                info = db.command(SON([("listCollections", 1)]))["cursor"]["firstBatch"]
                coll_info = next((c for c in info if c["name"] == collection_name), None)
                if coll_info and "options" in coll_info and "validator" in coll_info["options"]:
                    validator = coll_info["options"]["validator"]
                    validation_level = coll_info["options"].get("validationLevel", "strict")
                    validation_action = coll_info["options"].get("validationAction", "error")
                    console.print(f"\n🔹[bold]Nivel de validación:[/bold] {validation_level}")
                    console.print(f"🔹[bold]Acción de validación:[/bold] {validation_action}")
                    console.print("\n[bold]Reglas del validador:[/bold]")
                    console.print(validator)
                else:
                    console.print("\n⚠️ No hay reglas de validación definidas para esta colección")
            except Exception as e:
                console.print(f"\n❌[red]Error al obtener reglas: {e}[/red]")
        elif choice == "2":
            console.print("\n[bold]Agregar validación simple[/bold]")
            validator_input = console.input("Ingrese las reglas de validación (en formato JSON): ")
            try:
                validator = eval(validator_input)
                validation_level = console.input("Nivel de validación (strict/off) [strict]: ") or "strict"
                validation_action = console.input("Acción de validación (error/warn) [error]: ") or "error"
                db.command({
                    "collMod": collection_name,
                    "validator": validator,
                    "validationLevel": validation_level,
                    "validationAction": validation_action
                })
                console.print("\n✅[green]Reglas de validación actualizadas correctamente[/green]")
            except Exception as e:
                console.print(f"\n❌[red]Error al actualizar validación: {e}[/red]")
        elif choice == "3":
            console.print("\n[bold]Agregar validación con JSON Schema[/bold]")
            schema_input = console.input("Ingrese el esquema JSON: ")
            try:
                schema = eval(schema_input)
                validation_level = console.input("Nivel de validación (strict/off) [strict]: ") or "strict"
                validation_action = console.input("Acción de validación (error/warn) [error]: ") or "error"
                db.command({
                    "collMod": collection_name,
                    "validator": {"$jsonSchema": schema},
                    "validationLevel": validation_level,
                    "validationAction": validation_action
                })
                console.print("\n✅[green]Esquema JSON de validación actualizado correctamente[/green]")
            except Exception as e:
                console.print(f"\n❌[red]Error al actualizar esquema: {e}[/red]")
        elif choice == "4":
            console.print("\n[bold]Eliminar validación[/bold]")
            confirm = console.input("¿Está seguro de eliminar todas las reglas de validación? (s/n): ")
            if confirm.lower() == "s":
                try:
                    db.command({
                        "collMod": collection_name,
                        "validator": {},
                        "validationLevel": "off"
                    })
                    console.print("\n✅[green]Reglas de validación eliminadas correctamente[/green]")
                except Exception as e:
                    console.print(f"\n❌[red]Error al eliminar validación: {e}[/red]")
        elif choice == "5":
            console.print("\n[bold]Probar validación[/bold]")
            console.print("1. Insertar documento válido\n2. Insertar documento inválido")
            test_choice = console.input("Seleccione opción (1-2): ")
            doc_input = console.input("Documento (en formato JSON): ")
            try:
                doc = eval(doc_input)
                result = collection.insert_one(doc)
                if test_choice == "1":
                    console.print(f"\n✅[green]Documento insertado correctamente con _id: {result.inserted_id}[/green]")
                else:
                    console.print(f"\n⚠️[yellow]Documento insertado a pesar de las reglas (puede ser por nivel 'warn')[/yellow]")
            except Exception as e:
                console.print(f"\n❌[red]Error de validación (esperado): {e}[/red]")
        else:
            console.print("\n❌[red]Opción inválida. Intente nuevamente.[/red]")
        
        console.input("\nPresione Enter para continuar...")
        console.clear()
