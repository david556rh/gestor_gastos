from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.transaccion import Transaccion
from app.models.categoria import Categoria
from app.schemas.transaccion import TransaccionCreate, TransaccionUpdate


def _validar_categoria(db: Session, categoria_id, tipo):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if categoria.tipo != tipo:
        raise HTTPException(
            status_code=400,
            detail=f"La categoría es de tipo '{categoria.tipo.value}' pero la transacción es de tipo '{tipo.value}'"
        )
    return categoria


def get_transacciones(db: Session, usuario_id, tipo=None, categoria_id=None, fecha_inicio=None, fecha_fin=None):
    query = db.query(Transaccion).filter(Transaccion.usuario_id == usuario_id)

    if tipo:
        query = query.filter(Transaccion.tipo == tipo)
    if categoria_id:
        query = query.filter(Transaccion.categoria_id == categoria_id)
    if fecha_inicio:
        query = query.filter(Transaccion.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Transaccion.fecha <= fecha_fin)

    return query.order_by(Transaccion.fecha.desc()).all()


def get_transaccion_by_id(db: Session, transaccion_id, usuario_id):
    transaccion = db.query(Transaccion).filter(
        Transaccion.id == transaccion_id,
        Transaccion.usuario_id == usuario_id
    ).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion


def create_transaccion(db: Session, data: TransaccionCreate, usuario_id):
    _validar_categoria(db, data.categoria_id, data.tipo)

    transaccion = Transaccion(
        tipo=data.tipo,
        monto=data.monto,
        fecha=data.fecha,
        descripcion=data.descripcion,
        categoria_id=data.categoria_id,
        usuario_id=usuario_id
    )
    db.add(transaccion)
    db.commit()
    db.refresh(transaccion)
    return transaccion


def update_transaccion(db: Session, transaccion_id, data: TransaccionUpdate, usuario_id):
    transaccion = get_transaccion_by_id(db, transaccion_id, usuario_id)

    if data.categoria_id:
        _validar_categoria(db, data.categoria_id, transaccion.tipo)
        transaccion.categoria_id = data.categoria_id
    if data.monto is not None:
        transaccion.monto = data.monto
    if data.fecha is not None:
        transaccion.fecha = data.fecha
    if data.descripcion is not None:
        transaccion.descripcion = data.descripcion

    db.commit()
    db.refresh(transaccion)
    return transaccion


def delete_transaccion(db: Session, transaccion_id, usuario_id):
    transaccion = get_transaccion_by_id(db, transaccion_id, usuario_id)
    db.delete(transaccion)
    db.commit()