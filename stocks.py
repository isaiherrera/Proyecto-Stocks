from flask import (
    Blueprint, redirect, render_template, request, url_for
)

import db
from models import Productos, Proveedores
from templates.auth import login_required

bp = Blueprint('stocks', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('stocks/index.html')


def get_proveedores():
    proveedores = {}
    for proveedor in db.session.query(Proveedores).all():
        proveedores[proveedor.id_proveedor] = proveedor.nombre_empresa
    return proveedores


@bp.route('/inventario')
def inventario():
    return render_template("stocks/inventario.html", lista_productos=db.session.query(Productos).all(),
                           nombre_proveedores=get_proveedores())


@bp.route('/anadir-producto')
def add():
    return render_template('stocks/addProduct.html', proveedores=get_proveedores())


@bp.route('/crear-producto', methods=['POST'])
def crear():
    producto = Productos(desc_producto=request.form['contenido_descripcion'],
                         stock=request.form['contenido_stock'],
                         capacidad=request.form['contenido_capacidad'],
                         precio=request.form['contenido_precio'],
                         categoria=request.form['contenido_categoria'],
                         id_proveedor=request.form['contenido_proveedor'])

    db.session.add(producto)
    db.session.commit()
    return redirect(url_for('stocks.inventario'))


@bp.route('/eliminar-producto/<id>')
def eliminar(id):
    tarea = db.session.query(Productos).filter_by(id_producto=int(id)).delete()
    db.session.commit()
    return redirect(url_for('stocks.inventario'))


@bp.route('/informes')
def informes():
    todos_los_productos = db.session.query(Productos).all()
    labels = []
    values = []
    for producto in todos_los_productos:
        labels.append(producto.desc_producto)
        values.append(producto.stock)
    return render_template('stocks/informes.html', labels=labels, values=values)


@bp.route('/proveedores')
def proveedores():
    todos_los_proveedores = db.engine.execute("select nombre_empresa from proveedores")
    return render_template("stocks/proveedores.html", lista_proveedores=todos_los_proveedores)
