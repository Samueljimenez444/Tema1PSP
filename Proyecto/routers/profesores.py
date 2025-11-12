from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from routers.asignaturas import lista_asignaturas

router = APIRouter(
    prefix="/profesores",
    tags=["Profesores"]
)

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

def next_id():
    return max(p.id for p in profesores_db) + 1


@router.get("/")
def get_profesores():
    return profesores_db

@router.get("/{id}")
def get_profesor(id: int):
    for profesor in profesores_db:
        if profesor.id == id:
            return profesor
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

@router.get("/buscarDNI/{DNI}")
def get_profesor_dni(DNI: str):
    for profesor in profesores_db:
        if profesor.DNI == DNI:
            return profesor
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

@router.get("/buscarNombre/{nombre}")
def get_profesor_nombre(nombre: str):
    for profesor in profesores_db:
        if profesor.nombre == nombre:
            return profesor
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

@router.get("/buscarTelefono/{telefono}")
def get_profesor_telefono(telefono: str):
    for profesor in profesores_db:
        if profesor.telefono == telefono:
            return profesor
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

@router.post("/", status_code=201, response_model=Profesor)
def añadir_profesor(profesor: Profesor):
    profesor.id = next_id()
    profesores_db.append(profesor)
    return profesor

@router.put("/", response_model=Profesor)
def modificar_profesor(id: int, profesor: Profesor):
    for index, profesor_guardado in enumerate(profesores_db):
        if profesor_guardado.id == id:
            profesor.id = id
            profesores_db[index] = profesor
            return profesor
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

@router.delete("/{id}")
def borrar_profesor(id: int):
    for profesor_guardado in profesores_db:
        if profesor_guardado.id == id:
            profesores_db.remove(profesor_guardado)
            return {}
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

@router.get("/{id}/asignaturas")
def get_profesor_asignatura(id : int):
    for asignatura in lista_asignaturas:
            if asignatura.id_profesor == id:
                return asignatura
            raise HTTPException(status_code=404, detail="Asignatura no encontrada")
    raise HTTPException(status_code=404, detail="Profesor no encontrado")

