import db
from sqlalchemy import Column, Integer, String, Float


class Producto(db.Base):
    __tablename__ = 'producto'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(200), nullable=False)
    stock = Column(Integer, nullable=False)
    capacidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String(50), nullable=False)
    proveedor = Column(String(100), nullable=False)

    def __init__(self, descripcion, stock, capacidad, precio, categoria, proveedor):
        self.descripcion = descripcion
        self.stock = stock
        self.capacidad = capacidad
        self.precio = precio
        self.categoria = categoria
        self.proveedor = proveedor

    def __str__(self):
        return "Producto {}: {} {}".format(self.descripcion, self.id, self.categoria)


class Proveedor(db.Base):
    __tablename__ = 'proveedor'
    __table_args__ = {'sqlite_autoincrement': True}
    id_proveedor = Column(Integer, primary_key=True)
    nombre_empresa = Column(String(50), nullable=False)
    telefono = Column(Integer)
    direccion = Column(String)

    def __init__(self, nombre_empresa, telefono, direccion):
        self.nombre_empresa = nombre_empresa
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return "Proveedor {}: {} {}".format(self.nombre_empresa, self.id_proveedor, self.telefono, self.direccion)


class Usuario(db.Base):
    __tablename__ = 'usuario'
    __table_args__ = {'sqlite_autoincrement': True}
    id_usuario = Column(Integer, primary_key=True)
    correo = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def __init__(self, correo, password):
        self.correo = correo
        self.password = password
