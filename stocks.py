from flask import Blueprint, redirect, render_template, request, url_for, session
from templates.auth import login_required
import db
from models import Producto, Proveedor, Usuario
from db import get_db
from werkzeug.security import generate_password_hash

bp = Blueprint('stocks', __name__)


@bp.route('/')
@login_required
def index():
    # producto = db.session.execute(db.select(Producto).filter_by(id=id)).scalar_one()
    usuario = db.session.query(Usuario).filter(Usuario.id_usuario == session.get('id_usuario')).first()
    print(usuario.correo)
    return render_template('stocks/index.html', usuario=usuario.type)


@bp.route('/inventario')
def inventario():
    todos_los_productos = db.session.query(Producto).all()
    todos_los_proveedores = db.session.query(Proveedor).all()
    return render_template("stocks/inventario.html", lista_productos=todos_los_productos,
                           lista_proveedores=get_proveedores())


@bp.route('/inventarioProveedores')
def inventario_proveedores():
    return render_template('/stocks/inventarioProveedores')


def get_proveedores():
    proveedores = {}
    for proveedor in db.session.query(Proveedor).all():
        proveedores[proveedor.id_proveedor] = proveedor.nombre_empresa
    return proveedores


@bp.route('/anadir-producto')
def add_product():
    todos_los_proveedores = db.session.query(Proveedor).all()
    return render_template('stocks/addProduct.html', lista_proveedores=todos_los_proveedores)


@bp.route('/crear-producto', methods=['POST'])
def crear():
    proveedor = db.session.execute(
        db.select(Proveedor).filter_by(nombre_empresa=request.form.get('proveedor_elegido'))).scalar_one()
    print(proveedor)
    print(proveedor.id_proveedor)
    producto = Producto(descripcion=request.form['contenido_descripcion'],
                        stock=request.form['contenido_stock'],
                        capacidad=request.form['contenido_capacidad'],
                        pvp=request.form['contenido_PVP'],
                        precio=request.form['contenido_precio'],
                        categoria=request.form['contenido_categoria'],
                        id_proveedor=proveedor.id_proveedor)
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
def eliminar_producto(id):
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
    usuarios_proveedores = db.session.query(Usuario).filter
    return render_template("stocks/proveedores.html", lista_proveedores=todos_los_proveedores)


@bp.route('/anadir-proveedor')
def add_proveedor():
    return render_template('stocks/addProveedor.html')


@bp.route('/crear-proveedor', methods=['POST'])
def crear_proveedor():
    usuario = Usuario(correo=request.form['correo'],
                      password=generate_password_hash(request.form['password']),
                      type='proveedor')

    db.session.add(usuario)
    db.session.commit()
    print(usuario)
    proveedor = Proveedor(nombre_empresa=request.form['contenido_empresa'],
                          telefono=request.form['contenido_telefono'],
                          direccion=request.form['contenido_direccion'],
                          cif=request.form['contenido_cif'],
                          id_usuario=usuario.id_usuario)
    db.session.add(proveedor)
    db.session.commit()
    return redirect(url_for('stocks.proveedores'))


@bp.route('/eliminar-proveedor/<id>')
def eliminar_proveedor(id):
    proveedor = db.session.query(Proveedor).filter_by(id_proveedor=int(id)).first()
    db.session.query(Usuario).filter_by(id_usuario=proveedor.id_usuario).delete()
    db.session.query(Proveedor).filter_by(id_proveedor=int(id)).delete()

    db.session.commit()
    return redirect(url_for('stocks.proveedores'))


@bp.route('/usuarios')
def usuarios():
    todos_los_usuarios = db.session.query(Usuario).all()
    return render_template('stocks/usuarios.html', lista_usuarios=todos_los_usuarios)


@bp.route('/eliminar-usuario/<id>')
def eliminar_usuario(id):
    db.session.query(Usuario).filter_by(id_usuario=int(id)).delete()
    db.session.commit()
    return redirect(url_for('stocks.usuarios'))


@bp.route('/admin')
def admin():
    id_usuario = session.get('id_usuario')
    if id_usuario == 1:
        return render_template('stocks/admin.html')
    else:
        return render_template('stocks/index.html')
