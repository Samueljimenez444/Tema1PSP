from fastapi import FastAPI
from routers import asignaturas, profesores, auth_users

app = FastAPI(title="API de Asignaturas y Profesores")


app.include_router(asignaturas.router)
app.include_router(auth_users.router)
app.include_router(profesores.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Asignaturas y Profesores"}
