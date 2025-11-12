from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/asignaturas",
    tags=["Asignaturas"]
)

class Asignatura(BaseModel):
    id: int
    titulo: str
    num_horas: int
    id_profesor: int

lista_asignaturas = [
    Asignatura(id=1, titulo="Programacion", num_horas=10, id_profesor=3),
    Asignatura(id=2, titulo="Sistemas", num_horas=5, id_profesor=1),
    Asignatura(id=3, titulo="Moviles", num_horas=3, id_profesor=2)
]

def next_id():
    return max(a.id for a in lista_asignaturas) + 1


@router.get("/")
def buscar_asignaturas():
    return lista_asignaturas

@router.get("/id/{id}")
def buscar_asignaturas_id(id: int):
    for asignatura in lista_asignaturas:
        if asignatura.id == id:
            return asignatura
    raise HTTPException(status_code=404, detail="Asignatura no encontrada")

@router.get("/idProfesor/{id_profesor}")
def buscar_asignaturas_id_profesor(id_profesor: int):
    for asignatura in lista_asignaturas:
        if asignatura.id_profesor == id_profesor:
            return asignatura
    raise HTTPException(status_code=404, detail="Asignatura con ese profesor no encontrada")

@router.post("/", status_code=201, response_model=Asignatura)
def añadir_asignatura(asignatura: Asignatura):
    asignatura.id = next_id()
    lista_asignaturas.append(asignatura)
    return asignatura

@router.put("/", response_model=Asignatura)
def modificar_asignatura(id: int, asignatura: Asignatura):
    for index, asig_guardada in enumerate(lista_asignaturas):
        if asig_guardada.id == id:
            asignatura.id = id
            lista_asignaturas[index] = asignatura
            return asignatura
    raise HTTPException(status_code=404, detail="Asignatura no encontrada")

@router.delete("/{id}")
def borrar_asignatura(id: int):
    for asignatura_guardada in lista_asignaturas:
        if asignatura_guardada.id == id:
            lista_asignaturas.remove(asignatura_guardada)
            return {}
    raise HTTPException(status_code=404, detail="Asignatura no encontrada")
