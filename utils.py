from flask import session

import db
from models import Proveedor, Usuario, Producto


def todos_los_proveedores():
    return db.session.query(Proveedor).all()


def todos_los_usuarios():
    return db.session.query(Usuario).all()


def todos_los_productos():
    return db.session.query(Producto).all()


def get_proveedores():
    proveedores = {}
    for proveedor in todos_los_proveedores():
        proveedores[proveedor.id_proveedor] = proveedor.nombre_empresa
    return proveedores


def usuario():
    usuario = db.session.execute(db.select(Usuario).filter_by(id_usuario=session.get('id_usuario'))).scalar_one()
    return usuario


def tipo_de_usuario():
    return usuario().type
