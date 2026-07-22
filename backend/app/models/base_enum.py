import enum

class TipoTransaccion(str, enum.Enum):
    gasto = "gasto"
    ingreso = "ingreso"