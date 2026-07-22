from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from app.services import categoria_service

router = APIRouter(prefix="/categorias", tags=["Categorías"])

# UUID temporal de usuario mientras no hay autenticación (Sprint 1)
USUARIO_TEMP_ID = UUID("00000000-0000-0000-0000-000000000001")


@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return categoria_service.get_categorias(db)


@router.post("/", response_model=CategoriaResponse, status_code=201)
def crear_categoria(data: CategoriaCreate, db: Session = Depends(get_db)):
    return categoria_service.create_categoria(db, data, USUARIO_TEMP_ID)


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def actualizar_categoria(categoria_id: UUID, data: CategoriaUpdate, db: Session = Depends(get_db)):
    return categoria_service.update_categoria(db, categoria_id, data, USUARIO_TEMP_ID)


@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    categoria_service.delete_categoria(db, categoria_id, USUARIO_TEMP_ID)