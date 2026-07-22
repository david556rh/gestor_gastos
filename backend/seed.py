from app.db.database import SessionLocal
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.base_enum import TipoTransaccion
from uuid import UUID

USUARIO_TEMP_ID = UUID("00000000-0000-0000-0000-000000000001")

CATEGORIAS_PREDEFINIDAS = [
    {"nombre": "comida", "tipo": TipoTransaccion.gasto},
    {"nombre": "transporte", "tipo": TipoTransaccion.gasto},
    {"nombre": "salud", "tipo": TipoTransaccion.gasto},
    {"nombre": "vivienda", "tipo": TipoTransaccion.gasto},
    {"nombre": "entretenimiento", "tipo": TipoTransaccion.gasto},
    {"nombre": "educación", "tipo": TipoTransaccion.gasto},
    {"nombre": "otros gastos", "tipo": TipoTransaccion.gasto},
    {"nombre": "salario", "tipo": TipoTransaccion.ingreso},
    {"nombre": "otros ingresos", "tipo": TipoTransaccion.ingreso},
]

db = SessionLocal()

try:
    usuario_existente = db.query(Usuario).filter(Usuario.id == USUARIO_TEMP_ID).first()
    if not usuario_existente:
        usuario = Usuario(
            id=USUARIO_TEMP_ID,
            nombre="Usuario",
            email="usuario@temp.com"
        )
        db.add(usuario)
        db.commit()
        print("Usuario temporal creado")

    for cat_data in CATEGORIAS_PREDEFINIDAS:
        existente = db.query(Categoria).filter(
            Categoria.nombre == cat_data["nombre"],
            Categoria.usuario_id == None
        ).first()
        if not existente:
            categoria = Categoria(
                nombre=cat_data["nombre"],
                tipo=cat_data["tipo"],
                usuario_id=None
            )
            db.add(categoria)

    db.commit()
    print("Categorías predefinidas creadas")

finally:
    db.close()