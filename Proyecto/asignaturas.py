
import pydantic
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from Proyecto.asignaturas import Asignatura

app = FastAPI()

class Asignatura(BaseModel):
    id : int
    titulo : str
    num_horas : int
    id_profesor : int


lista_asignaturas = [
    Asignatura(id = 1, titulo="Programacion", num_horas=10, id_profesor=3),
    Asignatura(id = 2, titulo = "Sistemas" , num_horas=5, id_profesor = 1),
    Asignatura(id = 3 , titulo = "Moviles" , num_horas = 3 , id_profesor = 2)
]
def next_id():
    return max(asignatura.id for asignatura in lista_asignaturas) + 1

@app.get("/")
def root():
    return {"message": "API de asignaturas"}

@app.get("/asignaturas")
def buscar_asignaturas():   
    return lista_asignaturas

@app.get("/asignaturas/id/{id}")
def buscar_asignaturas_id(id : int):
    for asignatura in lista_asignaturas:
        if(asignatura.id == id):
            return asignatura
    raise HTTPException (status_code=404, detail="Asignatura con esa id no encontrado")

@app.get("/asignaturas/idProfesor/{id_profesor}")
def buscar_asignaturas_id_profesor(id_profesor : int):
    for asignatura in lista_asignaturas:
        if asignatura.id_profesor == id_profesor:
            return asignatura
    raise HTTPException (status_code=404, detail="Asignatura con esa id de profesor no encontrado")

@app.post("/asignatura" , status_code=201, response_model=Asignatura)
def añadir_profesor(asignatura : Asignatura):

    asignatura.id=next_id()

    lista_asignaturas.append(asignatura)

    return asignatura

@app.put("/asignatura" , response_model=Asignatura)
def modificar_profesor(id: int, asignatura: Asignatura):

        for index, asgnatura_guardada in enumerate(lista_asignaturas):
            if(asgnatura_guardada.id == id):
                asignatura.id=id
                lista_asignaturas[index] = asignatura
                return asignatura
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

@app.delete("/asignatura/{id}")
def borrar_profesor(id:int):
    for asignatura_guardada in lista_asignaturas:
        if asignatura_guardada.id == id:
            lista_asignaturas.remove(asignatura_guardada)
            return{}
    raise HTTPException(status_code=404 , detail="Profesor no encontrado")