from flask import Blueprint, redirect, render_template, request, url_for, session
from templates.auth import login_required
import db
from models import Producto, Proveedor, Usuario
from db import get_db
from werkzeug.security import generate_password_hash

bp = Blueprint('stocks', __name__)


def get_proveedores():
    proveedores = {}
    for proveedor in db.session.query(Proveedor).all():
        proveedores[proveedor.id_proveedor] = proveedor.nombre_empresa
    return proveedores


def tipo_de_usuario():
    usuario = db.session.execute(
        db.select(Usuario).filter_by(id_usuario=session.get('id_usuario'))).scalar_one()
    return usuario.type


@bp.route('/')
@login_required
def index():
    return render_template('stocks/index.html', tipo_de_usuario=tipo_de_usuario())


@bp.route('/inventario')
def inventario():
    todos_los_productos = db.session.query(Producto).all()
    todos_los_proveedores = db.session.query(Proveedor).all()
    return render_template("stocks/inventario/inventario.html", lista_productos=todos_los_productos,
                           lista_proveedores=get_proveedores(), tipo_de_usuario=tipo_de_usuario())


@bp.route('/anadir-producto')
def add_product():
    todos_los_proveedores = db.session.query(Proveedor).all()
    return render_template('stocks/inventario/addProduct.html', lista_proveedores=todos_los_proveedores)


@bp.route('/editar-producto/<id>')
def editar(id):
    producto = get_db().execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchone()

    return render_template('stocks/inventario/editProduct.html', producto=producto)


@bp.route('/editProduct/<id>', methods=['POST'])
def edit(id):
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


@bp.route('/crear-producto', methods=['POST'])
def crear():
    proveedor = db.session.execute(
        db.select(Proveedor).filter_by(nombre_empresa=request.form.get('proveedor_elegido'))).scalar_one()
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


@bp.route('/eliminar-producto/<id>')
def eliminar_producto(id):
    db.session.query(Producto).filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('stocks.inventario'))


@bp.route('/inventarioProveedor')
def inventario_proveedores():
    productos_proveedor = []
    get_proveedor = db.session.execute(
        db.select(Proveedor).filter_by(id_usuario=session.get('id_usuario'))).scalar_one()
    productos = db.session.execute(
        db.select(Producto).filter_by(id_proveedor=get_proveedor.id_proveedor)).scalars()
    for producto in productos:
        productos_proveedor.append(producto)
    return render_template('/stocks/proveedores/inventarioProveedor.html', productos_proveedor=productos_proveedor,
                           proveedor=get_proveedor)


@bp.route('/informes')
def informes():
    todos_los_productos = db.session.query(Producto).all()
    nombres_producto = []
    ventas = []
    beneficios = []
    productos_del_proveedor = []
    compras = []
    if tipo_de_usuario() == 'proveedor':
        get_proveedor = db.session.execute(
            db.select(Proveedor).filter_by(id_usuario=session.get('id_usuario'))).scalar_one()
        productos_proveedor = db.session.execute(
            db.select(Producto).filter_by(id_proveedor=get_proveedor.id_proveedor)).scalars()
        for producto in productos_proveedor:
            productos_del_proveedor.append(producto.descripcion)
            compras.append(producto.capacidad - producto.stock)
        return render_template('stocks/informes/informes.html', nombres_producto_proveedor=productos_del_proveedor,
                               compras=compras, tipo_de_usuario=tipo_de_usuario())
    else:
        for producto in todos_los_productos:
            nombres_producto.append(producto.descripcion)
            ventas.append(producto.capacidad - producto.stock)
            beneficios.append((producto.pvp - producto.precio) * (producto.capacidad - producto.stock))

        return render_template('stocks/informes/informes.html', nombres=nombres_producto, ventas=ventas,
                               beneficios=beneficios, tipo_de_usuario=tipo_de_usuario())


@bp.route('/proveedores')
def proveedores():
    todos_los_proveedores = db.session.query(Proveedor).all()
    todos_los_usuarios = db.session.query(Usuario).all()
    return render_template("stocks/proveedores/proveedores.html", lista_proveedores=todos_los_proveedores,
                           lista_usuarios=todos_los_usuarios)


@bp.route('/anadir-proveedor')
def add_proveedor():
    return render_template('stocks/proveedores/addProveedor.html')


@bp.route('/crear-proveedor', methods=['POST'])
def crear_proveedor():
    usuario = Usuario(correo=request.form['correo'],
                      password=generate_password_hash(request.form['password']),
                      type='proveedor')
    db.session.add(usuario)
    db.session.commit()
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
    return render_template('stocks/usuarios/usuarios.html', lista_usuarios=todos_los_usuarios)


@bp.route('/eliminar-usuario/<id>')
def eliminar_usuario(id):
    db.session.query(Usuario).filter_by(id_usuario=int(id)).delete()
    db.session.commit()
    return redirect(url_for('stocks.usuarios'))
