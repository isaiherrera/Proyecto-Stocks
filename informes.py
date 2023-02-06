from flask import render_template, redirect, url_for, Blueprint

import db
from models import Proveedor, Producto
from utils import tipo_de_usuario, todos_los_productos, usuario

bp = Blueprint('informes', __name__)


@bp.route('/informes')
def informes():
    nombres_producto = []
    ventas = []
    beneficios = []
    productos_del_proveedor = []
    compras = []
    if tipo_de_usuario() == 'proveedor':
        get_proveedor = db.session.execute(
            db.select(Proveedor).filter_by(id_usuario=db.session.get('id_usuario'))).scalar_one()
        productos_proveedor = db.session.execute(
            db.select(Producto).filter_by(id_proveedor=get_proveedor.id_proveedor)).scalars()
        for producto in productos_proveedor:
            productos_del_proveedor.append(producto.descripcion)
            compras.append(producto.capacidad - producto.stock)
        return render_template('informes/informes.html', nombres_producto_proveedor=productos_del_proveedor,
                               compras=compras, tipo_de_usuario=tipo_de_usuario(), usuario=usuario())
    else:
        for producto in todos_los_productos():
            nombres_producto.append(producto.descripcion)
            ventas.append(producto.capacidad - producto.stock)
            beneficios.append((producto.pvp - producto.precio) * (producto.capacidad - producto.stock))

        return render_template('informes/informes.html', nombres=nombres_producto, ventas=ventas,
                               beneficios=beneficios, tipo_de_usuario=tipo_de_usuario(), usuario=usuario())
