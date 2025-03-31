from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["escuela"]  # Crea la base de datos "escuela"
estudiantes = db["estudiantes"]  # Crea la colección "estudiantes"

# Insertar 5 documentos
estudiantes.insert_many([
    {"nombre": "Ana Amaya", "edad": 21, "curso": "Física", "nota": 8.4},
    {"nombre": "Estiven Ramirez", "edad": 30, "curso": "Matemáticas", "nota": 9.3},
    {"nombre": "María Puertas", "edad": 19, "curso": "Biologia", "nota": 7.8},
    {"nombre": "David Escobar", "edad": 25, "curso": "Matemáticas", "nota": 8.5},
    {"nombre": "Fernanda Patoja", "edad": 20, "curso": "Física", "nota": 5.8},
])

# Encontrar estudiantes con nota mayor a 8
estudiantes_nota_mayor_8 = estudiantes.find({"nota": {"$gt": 8}})
print("Estudiantes con nota mayor a 8:")
for estudiante in estudiantes_nota_mayor_8:
    print(estudiante)

# Encontrar estudiantes de 20 años
estudiantes_20_años = estudiantes.find({"edad": 20})
print("\nEstudiantes de 20 años:")
for estudiante in estudiantes_20_años:
    print(estudiante)

# Actualizar la nota de "Ana" a 9.5
estudiantes.update_one({"nombre": "Ana Amaya"}, {"$set": {"nota": 9.5}})

# Incrementar la edad de todos los estudiantes en 1 año
estudiantes.update_many({}, {"$inc": {"edad": 1}})

# Encontrar estudiantes con nota entre 7 y 9 y menos de 22 años
estudiantes_filtrados = estudiantes.find({
    "nota": {"$gte": 7, "$lte": 9},
    "edad": {"$lt": 22},
})
print("\nEstudiantes con nota entre 7 y 9 y menos de 22 años:")
for estudiante in estudiantes_filtrados:
    print(estudiante)

# Calcular el promedio de las notas
promedio_notas = estudiantes.aggregate([{"$group": {"_id": None, "promedio": {"$avg": "$nota"}}}])
promedio = list(promedio_notas)[0]["promedio"]
print(f"\nPromedio de notas: {promedio}")

# Agrupar por curso y calcular el promedio por curso
promedio_por_curso = estudiantes.aggregate([
    {"$group": {"_id": "$curso", "promedio": {"$avg": "$nota"}}}
])
print("\nPromedio de notas por curso:")
for curso in promedio_por_curso:
    print(f"Curso: {curso['_id']}, Promedio: {curso['promedio']}")

# Crear un índice en el campo "curso"
estudiantes.create_index("curso")
print("\nÍndice creado en el campo 'curso'")

# Consulta que utiliza el índice
estudiantes_matematicas = estudiantes.find({"curso": "Matemáticas"})
print("\nEstudiantes de Matemáticas (usando el índice):")
for estudiante in estudiantes_matematicas:
    print(estudiante)

# Eliminar estudiantes con nota menor a 6
estudiantes.delete_many({"nota": {"$lt": 6}})
print("\nEstudiantes con nota menor a 6 eliminados.")

# Crear la colección "cursos"
cursos = db["cursos"]

# Insertar documentos en la colección "cursos"
cursos.insert_many([
    {"nombre": "Matemáticas", "estudiantes": ["Estiven Ramirez", "David Escobar"]},
    {"nombre": "Física", "estudiantes": ["Ana Amaya", "Fernanda Patoja"]},
    {"nombre": "Biologia", "estudiantes": ["María Puertas"]},
])

# Encontrar cursos en los que está inscrito un estudiante específico
estudiante_buscar = "María Puertas"
cursos_inscritos = cursos.find({"estudiantes": estudiante_buscar})
print(f"\nCursos en los que está inscrito {estudiante_buscar}:")
for curso in cursos_inscritos:
    print(curso["nombre"])

# Cerrar la conexión
client.close()