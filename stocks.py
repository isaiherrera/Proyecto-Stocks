from flask import Blueprint, redirect, render_template, request, url_for, session, abort

import db
from auth import login_required
from models import Producto, Proveedor, Usuario
from utils import tipo_de_usuario, usuario, get_proveedores, todos_los_proveedores, todos_los_productos

bp = Blueprint('stocks', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('index.html', tipo_de_usuario=tipo_de_usuario(), usuario=usuario())


@bp.route('/inventario')
def inventario():
    return render_template("inventario/inventario.html", lista_productos=todos_los_productos(),
                           lista_proveedores=get_proveedores(), tipo_de_usuario=tipo_de_usuario(), usuario=usuario())


@bp.route('/editar-producto/<id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'GET':
        producto = db.session.query(Producto).filter_by(id=id).first()
        return render_template('inventario/editProduct.html', producto=producto,
                               lista_proveedores=get_proveedores(), usuario=usuario())
    if request.method == 'POST':
        producto = db.session.execute(db.select(Producto).filter_by(id=id)).scalar_one()
        producto.descripcion = request.form['new_descripcion']
        producto.stock = request.form['new_stock']
        producto.capacidad = request.form['new_capacidad']
        producto.pvp = request.form['new_PVP']
        producto.precio = request.form['new_precio']
        producto.categoria = request.form['new_categoria']
        producto.proveedor = request.form['new_proveedor']

        db.session.commit()

        return redirect(url_for('stocks.inventario'))


@bp.route('/anadir-producto', methods=['GET', 'POST'])
def add_product():
    if request.method == 'GET':
        return render_template('inventario/anadir-producto.html', lista_proveedores=get_proveedores(),
                               usuario=usuario())
    if request.method == 'POST':
        producto = Producto(descripcion=request.form['contenido_descripcion'],
                            stock=request.form['contenido_stock'],
                            capacidad=request.form['contenido_capacidad'],
                            pvp=request.form['contenido_PVP'],
                            precio=request.form['contenido_precio'],
                            categoria=request.form['contenido_categoria'],
                            id_proveedor=request.form['proveedor_elegido'])
        db.session.add(producto)
        db.session.commit()
        return redirect(url_for('stocks.inventario'))


@bp.route('/eliminar-producto/<id>')
def eliminar_producto(id):
    del_producto = db.session.query(Producto).filter_by(id=int(id)).delete()
    if del_producto < 0:
        return abort(code=404)
    else:
        db.session.commit()
        return redirect(url_for('stocks.inventario'))
