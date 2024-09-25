# API REST: Interfaz de Programación de aplicaciones para compratir/transferir recursos

from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# FastAPI Biblioteca o Framework

# Inicializamos una variable que tendrá las características de Fast API REST
app = FastAPI()

# Acá definimos el modelo
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Simularemos una base de datos
cursos_db = []

# CRUD - Read (leer) GET ALL: Leeeremos todos los cursos que haya en la db

@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return cursos_db

# CRUD - Create (crear) POST: agregamos un nuevo recurso a nuestra base de datos
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) # Usamos UUID para generar un ID único e irrepetible
    cursos_db.append(curso)
    return curso

# CRUD: Read (leer) GET (individual): leeremos el curso que coincida con el ID que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

# CRUD : Update (Actualizar/Modificar) PUT: Modificaremos un recurso que coincida con el ID que mandemos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
        curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
        if curso is None:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        curso_actualizado.id = curso_id
        index = cursos_db.index(curso) # Buscamos el indice exacto donde está el curso en nuestra lista (DB)
        cursos_db[index] = curso_actualizado
        return curso_actualizado

# CRUD: Delete (borrar/baja) Eliminaremos un recurso que coincida con el ID que mandemos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso
