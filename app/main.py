from fastapi import FastAPI
from app.routers import categorias, transacciones

app = FastAPI(
    title="Gestor de Gastos API",
    description="API REST para el gestor de gastos personales",
    version="1.0.0"
)

app.include_router(categorias.router)
app.include_router(transacciones.router)


@app.get("/")
def root():
    return {"mensaje": "Gestor de Gastos API funcionando"}