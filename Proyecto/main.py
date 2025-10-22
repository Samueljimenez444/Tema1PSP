from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi import HTTPException


app = FastAPI()

class Profesor(BaseModel):
    id: Optional[int] = None
    DNI: str
    nombre: str
    apellidos: str
    telefono: str
    direccion: str
    cuentaBancaria: str

profesores_db = [
    Profesor(id=1, DNI="123432456A", nombre="Fernando", apellidos="Galiana", telefono="654123456", direccion="Calle Victor Torres", cuentaBancaria="ES3424234234"),
    Profesor(id=2, DNI="654646747B", nombre="David", apellidos="Bermudez", telefono="654987654", direccion="Avenida Nervion", cuentaBancaria="ES654765873"),
    Profesor(id=3, DNI="11111111C", nombre="Elena", apellidos="Rivero", telefono="654456789", direccion="Plaza España", cuentaBancaria="ES14342443244")
]

@app.get("/")
def root():
    return {"message": "API de Profesores"}

@app.get("/profesores")
def get_profesores():
    return profesores_db

@app.get("/profesores/{id}")
def get_profesor(id: int):
    for profesor in profesores_db:
        if profesor.id == id:
            return profesor
    return {"error": "Profesor no encontrado"}

@app.get("/profesores/buscarDNI/{DNI}")
def get_profesor_dni(DNI: str):
    for profesor in profesores_db:
        if profesor.DNI == DNI:
            return profesor
    return {"error": "Profesor no encontrado"}

@app.get("/profesores/buscarNombre/{nombre}")
def get_profesor_nombre(nombre: str):
    for profesor in profesores_db:
        if profesor.nombre == nombre:
            return profesor
    return {"error": "Profesor no encontrado"}

@app.get("/profesores/buscarTelefono/{telefono}")
def get_profesor_telefono(telefono: str):
    for profesor in profesores_db:
        if profesor.telefono == telefono:
            return profesor
    return {"error": "Profesor no encontrado"}

@app.get("/profesores/")
def get_query_telefo_dni(dni: str):
    for profesor in profesores_db:
        if profesor.DNI == dni:
            return profesor
    return {"error": "No hay un profesor con esas características"}

def next_id():
    return max(profesor.id for profesor in profesores_db) + 1
    

@app.post("/profesores" , status_code=201, response_model=Profesor)
def añadir_profesor(profesor: Profesor):

    profesor.id=next_id()

    profesores_db.append(profesor)

    return profesor

@app.put("/profesores" , response_model=Profesor)
def modificar_profesor(id: int, profesor: Profesor):

        for index, profesor_guardado in enumerate(profesores_db):
            if(profesor_guardado.id == id):
                profesor.id=id
                profesores_db[index] = profesor
                return profesor
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
        
@app.delete("/profesores/{id}")
def borrar_profesor(id:int):
    for profesor_guardado in profesores_db:
        if profesor_guardado.id == id:
            profesores_db.remove(profesor_guardado)
            return{}
    raise HTTPException(status_code=404 , detail="Profesor no encontrado")

