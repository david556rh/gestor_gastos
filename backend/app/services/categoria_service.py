from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


def get_categorias(db: Session):
    return db.query(Categoria).all()


def get_categoria_by_id(db: Session, categoria_id):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


def create_categoria(db: Session, data: CategoriaCreate, usuario_id):
    # RN-06: nombre único por usuario (case-insensitive, ya normalizado por el schema)
    existente = db.query(Categoria).filter(
        func.lower(Categoria.nombre) == data.nombre,
        Categoria.usuario_id == usuario_id
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")

    categoria = Categoria(
        nombre=data.nombre,
        tipo=data.tipo,
        usuario_id=usuario_id
    )
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def update_categoria(db: Session, categoria_id, data: CategoriaUpdate, usuario_id):
    categoria = get_categoria_by_id(db, categoria_id)

    # RN-04: solo se pueden editar categorías personalizadas del usuario
    if categoria.usuario_id is None:
        raise HTTPException(status_code=403, detail="Las categorías del sistema no se pueden editar")
    if categoria.usuario_id != usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta categoría")

    # RN-06: nombre único
    existente = db.query(Categoria).filter(
        func.lower(Categoria.nombre) == data.nombre,
        Categoria.usuario_id == usuario_id,
        Categoria.id != categoria_id
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")

    categoria.nombre = data.nombre
    db.commit()
    db.refresh(categoria)
    return categoria


def delete_categoria(db: Session, categoria_id, usuario_id):
    categoria = get_categoria_by_id(db, categoria_id)

    # RN-04: solo categorías personalizadas del usuario
    if categoria.usuario_id is None:
        raise HTTPException(status_code=403, detail="Las categorías del sistema no se pueden eliminar")
    if categoria.usuario_id != usuario_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta categoría")

    # RN-05: no se puede eliminar si tiene transacciones asociadas
    if categoria.transacciones:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar una categoría que tiene transacciones asociadas"
        )

    db.delete(categoria)
    db.commit()
