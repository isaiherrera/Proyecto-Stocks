from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from templates.auth import login_required
import db
from db import get_db
from models import Producto, Proveedor

bp = Blueprint('stocks', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('stocks/index.html')


@bp.route('/inventario')
def inventario():
    todos_los_productos = db.session.query(Producto).all()
    return render_template("stocks/inventario.html", lista_productos=todos_los_productos, porcentaje=porcentaje_stock)


def porcentaje_stock(self):
    return (self.stock / self.cantidad) * 100


@bp.route('/anadir-producto')
def add():
    return render_template('stocks/addProduct.html')


@bp.route('/crear-producto', methods=['POST'])
def crear():
    producto = Producto(descripcion=request.form['contenido_descripcion'],
                        stock=request.form['contenido_stock'], cantidad=request.form['contenido_cantidad'],
                        precio=request.form['contenido_precio'],
                        categoria=request.form['contenido_categoria'], proveedor=request.form['contenido_proveedor'])
    db.session.add(producto)
    db.session.commit()
    return redirect(url_for('stocks.inventario'))


@bp.route('/eliminar-producto/<id>')
def eliminar(id):
    tarea = db.session.query(Producto).filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('stocks.inventario'))


@bp.route('/informes')
def informes():
    return render_template('stocks/informes.html')


@bp.route('/proveedores')
def proveedores():
    todos_los_proveedores = db.session.query(Proveedor).all()
    return render_template("stocks/proveedores.html", lista_proveedores=todos_los_proveedores)
