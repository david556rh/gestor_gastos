from pydantic import BaseModel, field_validator
from uuid import UUID
from app.models.base_enum import TipoTransaccion


class CategoriaCreate(BaseModel):
    nombre: str
    tipo: TipoTransaccion

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip().lower()


class CategoriaUpdate(BaseModel):
    nombre: str

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip().lower()


class CategoriaResponse(BaseModel):
    id: UUID
    nombre: str
    tipo: TipoTransaccion
    usuario_id: UUID | None

    model_config = {"from_attributes": True}