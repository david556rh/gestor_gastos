from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date
from app.db.database import get_db
from app.schemas.transaccion import TransaccionCreate, TransaccionUpdate, TransaccionResponse
from app.services import transaccion_service
from app.models.base_enum import TipoTransaccion

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

USUARIO_TEMP_ID = UUID("00000000-0000-0000-0000-000000000001")


@router.get("/", response_model=list[TransaccionResponse])
def listar_transacciones(
    tipo: TipoTransaccion | None = Query(None),
    categoria_id: UUID | None = Query(None),
    fecha_inicio: date | None = Query(None),
    fecha_fin: date | None = Query(None),
    db: Session = Depends(get_db)
):
    return transaccion_service.get_transacciones(
        db, USUARIO_TEMP_ID, tipo, categoria_id, fecha_inicio, fecha_fin
    )


@router.post("/", response_model=TransaccionResponse, status_code=201)
def crear_transaccion(data: TransaccionCreate, db: Session = Depends(get_db)):
    return transaccion_service.create_transaccion(db, data, USUARIO_TEMP_ID)


@router.get("/{transaccion_id}", response_model=TransaccionResponse)
def obtener_transaccion(transaccion_id: UUID, db: Session = Depends(get_db)):
    return transaccion_service.get_transaccion_by_id(db, transaccion_id, USUARIO_TEMP_ID)


@router.put("/{transaccion_id}", response_model=TransaccionResponse)
def actualizar_transaccion(transaccion_id: UUID, data: TransaccionUpdate, db: Session = Depends(get_db)):
    return transaccion_service.update_transaccion(db, transaccion_id, data, USUARIO_TEMP_ID)


@router.delete("/{transaccion_id}", status_code=204)
def eliminar_transaccion(transaccion_id: UUID, db: Session = Depends(get_db)):
    transaccion_service.delete_transaccion(db, transaccion_id, USUARIO_TEMP_ID)