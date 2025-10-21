from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Profesor(BaseModel):
    id: int
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