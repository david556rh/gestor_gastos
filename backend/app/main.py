from fastapi import FastAPI

app = FastAPI(
    title="Gestor de Gastos API",
    description="API REST para el gestor de gastos personales",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"mensaje": "Gestor de Gastos API funcionando"}