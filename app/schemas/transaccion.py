from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import date
from decimal import Decimal
from app.models.base_enum import TipoTransaccion


class TransaccionCreate(BaseModel):
    tipo: TipoTransaccion
    monto: Decimal
    fecha: date
    descripcion: str | None = None
    categoria_id: UUID

    @field_validator("monto")
    @classmethod
    def monto_positivo(cls, v):
        if v <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        return v

    @field_validator("fecha")
    @classmethod
    def fecha_no_futura(cls, v):
        if v > date.today():
            raise ValueError("La fecha no puede ser posterior a hoy")
        return v


class TransaccionUpdate(BaseModel):
    monto: Decimal | None = None
    fecha: date | None = None
    descripcion: str | None = None
    categoria_id: UUID | None = None

    @field_validator("monto")
    @classmethod
    def monto_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        return v

    @field_validator("fecha")
    @classmethod
    def fecha_no_futura(cls, v):
        if v is not None and v > date.today():
            raise ValueError("La fecha no puede ser posterior a hoy")
        return v


class TransaccionResponse(BaseModel):
    id: UUID
    tipo: TipoTransaccion
    monto: Decimal
    fecha: date
    descripcion: str | None
    categoria_id: UUID
    usuario_id: UUID

    model_config = {"from_attributes": True}