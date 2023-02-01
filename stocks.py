from flask import Blueprint, redirect, render_template, request, url_for, session
from templates.auth import login_required
import db
from models import Producto, Proveedor, Usuario
from db import get_db

bp = Blueprint('stocks', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('stocks/index.html')


@bp.route('/inventario')
def inventario():
    todos_los_productos = db.session.query(Producto).all()
    return render_template("stocks/inventario.html", lista_productos=todos_los_productos)


def porcentaje_stock(self):
    return (self.stock / self.cantidad) * 100


@bp.route('/anadir-producto')
def add_product():
    return render_template('stocks/addProduct.html')


@bp.route('/crear-producto', methods=['POST'])
def crear():
    producto = Producto(descripcion=request.form['contenido_descripcion'],
                        stock=request.form['contenido_stock'],
                        capacidad=request.form['contenido_capacidad'],
                        pvp=request.form['contenido_PVP'],
                        precio=request.form['contenido_precio'],
                        categoria=request.form['contenido_categoria'],
                        proveedor=request.form['contenido_proveedor'])

    db.session.add(producto)
    db.session.commit()
    return redirect(url_for('stocks.inventario'))


@bp.route('/editar-producto/<id>')
def editar(id):
    producto = get_db().execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()
    print(producto)
    return render_template('stocks/editProduct.html', producto=producto)


@bp.route('/editProduct/<id>', methods=['POST'])
def edit(id):
    producto = db.session.execute(db.select(Producto).filter_by(id=id)).scalar_one()
    print(producto)

    producto.descripcion = request.form['new_descripcion']
    producto.stock = request.form['new_stock']
    producto.capacidad = request.form['new_capacidad']
    producto.pvp = request.form['new_PVP']
    producto.precio = request.form['new_precio']
    producto.categoria = request.form['new_categoria']
    producto.proveedor = request.form['new_proveedor']

    db.session.commit()
    print(producto)
    return redirect(url_for('stocks.inventario'))


@bp.route('/eliminar-producto/<id>')
def eliminar(id):
    db.session.query(Producto).filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('stocks.inventario'))


@bp.route('/informes')
def informes():
    todos_los_productos = db.session.query(Producto).all()
    labels = []
    values = []
    for producto in todos_los_productos:
        labels.append(producto.descripcion)
        values.append(producto.stock)
    return render_template('stocks/informes.html', labels=labels, values=values)


@bp.route('/proveedores')
def proveedores():
    todos_los_proveedores = db.session.query(Proveedor).all()
    return render_template("stocks/proveedores.html", lista_proveedores=todos_los_proveedores)


@bp.route('/anadir-proveedor')
def add_proveedor():
    return render_template('stocks/addProveedor.html')


@bp.route('/crear-proveedor', methods=['POST'])
def crear_proveedor():
    usuario = Usuario(correo=request.form['correo'],
                      password=request.form['password'])
    proveedor = Proveedor(nombre_empresa=request.form['contenido_empresa'],
                          telefono=request.form['contenido_telefono'],
                          direccion=request.form['contenido_direccion'],
                          cif=request.form['contenido_cif'])
    db.session.add(usuario)
    db.session.add(proveedor)
    db.session.commit()
    return redirect(url_for('stocks.inventario'))


@bp.route('/admin')
def admin():
    id_usuario = session.get('id_usuario')
    if id_usuario == 1:
        return render_template('stocks/admin.html')
    else:
        return render_template('stocks/index.html')
