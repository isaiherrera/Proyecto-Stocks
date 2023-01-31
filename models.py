import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class Productos(db.Base):
    __tablename__ = 'productos'
    __table_args__ = {'sqlite_autoincrement': True}
    id_producto = Column(Integer, primary_key=True)
    desc_producto = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    capacidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)
    id_proveedor = Column(String, ForeignKey("proveedores.id_proveedor"), nullable=False)

    def __init__(self, desc_producto, stock, capacidad, precio, categoria, id_proveedor):
        self.desc_producto = desc_producto
        self.stock = stock
        self.capacidad = capacidad
        self.precio = precio
        self.categoria = categoria
        self.id_proveedor = id_proveedor

    def __str__(self):
        return "Producto {}: {} {}".format(self.desc_producto, self.id_producto, self.categoria)


class Proveedores(db.Base):
    __tablename__ = 'proveedores'
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


class TiposUsuarios(db.Base):
    __tablename__ = 'tipos_usuarios'
    __table_args__ = {'sqlite_autoincrement': True}
    id_tipo_usuario = Column(Integer, primary_key=True)
    nombre_tipo_usuario = Column(String)


class Usuarios(db.Base):
    __tablename__ = 'usuarios'
    __table_args__ = {'sqlite_autoincrement': True}
    id_usuario = Column(Integer, primary_key=True)
    correo = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    tipo_usuario = Column(Integer, ForeignKey("tipos_usuarios.id_tipo_usuario"), nullable=False)

    def __init__(self, correo, password, tipo_usuario):
        self.correo = correo
        self.password = password
        self.tipo_usuario = tipo_usuario


class Ventas(db.Base):
    __tablename__ = 'ventas'
    __table_args__ = {'sqlite_autoincrement': True}
    id_venta = Column(Integer, primary_key=True)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id_proveedor"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    precio = Column(Float, ForeignKey("productos.precio"), nullable=False)
    desc_producto = Column(String, ForeignKey("productos.desc_producto"), nullable=False)
    desc_venta = Column(String)

    def __init__(self, desc_venta):
        self.desc_venta = desc_venta
