import uuid
from sqlalchemy import Column, String, Numeric, Date, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.base_enum import TipoTransaccion


class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipo = Column(Enum(TipoTransaccion), nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    fecha = Column(Date, nullable=False)
    descripcion = Column(String(500), nullable=True)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("categorias.id"), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    categoria = relationship("Categoria", back_populates="transacciones")
    usuario = relationship("Usuario", back_populates="transacciones")