from bbdd import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class Usuario(db.Base):
    __tablename__ = 'usuario'
    __table_args__ = {'sqlite_autoincrement': True}
    id_usuario = Column(Integer, primary_key=True)
    correo = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    type = Column(String)

    def __init__(self, correo, password, type):
        self.correo = correo
        self.password = password
        self.type = type


class Proveedor(db.Base):
    __tablename__ = 'proveedor'
    __table_args__ = {'sqlite_autoincrement': True}
    id_proveedor = Column(Integer, primary_key=True)
    nombre_empresa = Column(String(50), nullable=False, unique=True)
    telefono = Column(Integer, nullable=False)
    direccion = Column(String, nullable=False)
    cif = Column(Integer, nullable=False, unique=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)

    def __init__(self, nombre_empresa, telefono, direccion, cif, id_usuario):
        self.nombre_empresa = nombre_empresa
        self.telefono = telefono
        self.direccion = direccion
        self.cif = cif
        self.id_usuario = id_usuario

    def __str__(self):
        return "Proveedor {}: {} {}".format(self.nombre_empresa, self.id_proveedor, self.telefono, self.direccion)


class Producto(db.Base):
    __tablename__ = 'producto'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(200), nullable=False, unique=True)
    stock = Column(Integer, nullable=False)
    capacidad = Column(Integer, nullable=False)
    pvp = Column(Float, nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String(50), nullable=False)
    id_proveedor = Column(Integer, ForeignKey('proveedor.id_proveedor'))

    def __init__(self, descripcion, stock, capacidad, pvp, precio, categoria, id_proveedor):
        self.descripcion = descripcion
        self.stock = stock
        self.capacidad = capacidad
        self.pvp = pvp
        self.precio = precio
        self.categoria = categoria
        self.id_proveedor = id_proveedor

    def __str__(self):
        return "Producto {}: {} {}".format(self.descripcion, self.id, self.categoria)
