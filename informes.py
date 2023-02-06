from flask import render_template, Blueprint, session

from bbdd import db
from bbdd.models import Proveedor, Producto
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
        get_proveedor = db.session.query(Proveedor.id_proveedor).filter_by(id_usuario=session['id_usuario']).first()[0]
        productos_proveedor = db.session.query(Producto).filter_by(id_proveedor=get_proveedor).all()
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
