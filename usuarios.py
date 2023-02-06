from flask import render_template, redirect, url_for, Blueprint

import db
from models import Usuario
from utils import usuario

bp = Blueprint('usuarios', __name__)


@bp.route('/usuarios')
def usuarios():
    clientes = db.session.execute(
        db.select(Usuario).filter_by(type='cliente')).scalars()
    return render_template('/usuarios/usuarios.html', lista_clientes=clientes, usuario=usuario())


@bp.route('/eliminar-usuario/<id>')
def eliminar_usuario(id):
    db.session.query(Usuario).filter_by(id_usuario=int(id)).delete()
    db.session.commit()
    return redirect(url_for('usuarios.usuarios'))
