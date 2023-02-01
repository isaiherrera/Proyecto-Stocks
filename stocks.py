from flask import Blueprint, redirect, render_template, request, url_for, session

import db
from models import Productos, Proveedores
from templates.auth import login_required
from db import get_db
from sqlalchemy import select
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
                           proveedores=get_proveedores())


@bp.route('/create-producto', methods=['GET', 'POST'])
def add_product():
    if request.method == 'GET':
        return render_template('stocks/create-producto.html', proveedores=get_proveedores())
    if request.method == 'POST':
        producto = Productos(desc_producto=request.form['contenido_descripcion'],
                             stock=request.form['contenido_stock'],
                             capacidad=request.form['contenido_capacidad'],
                             precio=request.form['contenido_precio'],
                             categoria=request.form['contenido_categoria'],
                             id_proveedor=request.form['contenido_proveedor'])

        db.session.add(producto)
        db.session.commit()
        return redirect(url_for('stocks.inventario'))


@bp.route('/editar-producto/<id_producto>', methods=['GET', 'POST'])
def update(id_producto):
    if request.method == 'GET':
        producto = db.session.query(Productos).filter(Productos.id_producto == id_producto).first()
        return render_template('stocks/editar-producto.html', producto=producto, proveedores=get_proveedores())
    if request.method == 'POST':
        db.session.query(Productos).filter(Productos.id_producto == id_producto).update({
            Productos.desc_producto: request.form['new_descripcion'],
            Productos.stock: request.form['new_stock'],
            Productos.capacidad: request.form['new_capacidad'],
            Productos.precio: request.form['new_precio'],
            Productos.categoria: request.form['new_categoria'],
            Productos.id_proveedor: request.form['new_proveedor']
        })
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
    todos_los_proveedores = db.session.query(Proveedores).all()
    todos_los_productos = db.session.query(Productos).all()
    num_productos = {}
    for proveedor in todos_los_proveedores:
        num_productos[proveedor.id_proveedor] = db.session.query(Productos).filter(
            Productos.id_proveedor == proveedor.id_proveedor).count()
    return render_template("stocks/proveedores.html", lista_proveedores=todos_los_proveedores,
                           num_productos=num_productos)


@bp.route('/admin')
def admin():
    id_usuario = session.get('id_usuario')
    if id_usuario == 1:
        return render_template('stocks/admin.html')
    else:
        return render_template('stocks/index.html')
