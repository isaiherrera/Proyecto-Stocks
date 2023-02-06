from flask import Blueprint, redirect, render_template, request, url_for, session
from werkzeug.security import generate_password_hash

import db
import utils
from models import Proveedor, Usuario, Producto
from utils import todos_los_proveedores, usuario, todos_los_usuarios

bp = Blueprint('proveedores', __name__, url_prefix='/proveedores')


@bp.route('/')
def proveedores():
    return render_template("proveedores/proveedores.html", lista_proveedores=todos_los_proveedores(),
                           lista_usuarios=todos_los_usuarios(), usuario=usuario())


@bp.route('/inventarioProveedor')
def inventario_proveedores():
    productos_proveedor = []
    get_proveedor = db.session.execute(
        db.select(Proveedor).filter_by(id_usuario=session.get('id_usuario'))).scalar_one()
    productos = db.session.execute(
        db.select(Producto).filter_by(id_proveedor=get_proveedor.id_proveedor)).scalars()
    for producto in productos:
        productos_proveedor.append(producto)
    return render_template('/proveedores/inventarioProveedor.html', productos_proveedor=productos_proveedor,
                           proveedor=get_proveedor, usuario=usuario())


@bp.route('/anadir-proveedor', methods=['GET', 'POST'])
def add_proveedor():
    if request.method == 'GET':
        return render_template('proveedores/anadir-proveedor.html', lista_proveedores=todos_los_proveedores(),
                               usuario=utils.usuario())
    if request.method == 'POST':
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
        return redirect(url_for('proveedores.proveedores'))


@bp.route('/eliminar-proveedor/<id>')
def eliminar_proveedor(id):
    proveedor = db.session.query(Proveedor).filter_by(id_proveedor=int(id)).first()
    db.session.query(Usuario).filter_by(id_usuario=proveedor.id_usuario).delete()
    db.session.query(Proveedor).filter_by(id_proveedor=int(id)).delete()
    db.session.commit()
    return redirect(url_for('proveedores.proveedores'), code=202)
