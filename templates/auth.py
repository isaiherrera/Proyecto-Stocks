import functools

from models import Usuarios
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
import db
from db import get_db
from models import TiposUsuarios

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # db.engine.execute("INSERT INTO tipos_usuarios (nombre_tipo_usuario) VALUES ('admin')")
    # db.engine.execute("INSERT INTO tipos_usuarios (nombre_tipo_usuario) VALUES ('cliente')")
    # db.engine.execute("INSERT INTO tipos_usuarios (nombre_tipo_usuario) VALUES ('proveedor')")
    # db.engine.execute("INSERT INTO proveedores (nombre_empresa, telefono, direccion) VALUES ('amazon', '654321987', 'calle falsa 123')")
    # db.engine.execute("INSERT INTO proveedores (nombre_empresa, telefono, direccion) VALUES ('bestbuy', '654321987', 'calle falsa 123')")
    # db.engine.execute("INSERT INTO proveedores (nombre_empresa, telefono, direccion) VALUES ('walmart', '654321987', 'calle falsa 123')")
    if request.method == 'POST':
        usuario = Usuarios(correo=request.form['correo'],
                           password=request.form['password'],
                           tipo_usuario=int(request.form['select_tipo_usuario']))
        print(f"correo\t{usuario.correo}")
        print(f"password\t{usuario.password}")
        error = None

        if not usuario.correo:
            error = 'Username is required.'
        elif not usuario.password:
            error = 'Password is required.'
        elif not usuario.tipo_usuario:
            error = 'tipo usuario is required.'

        if error is None:
            try:
                db.engine.execute(
                    "INSERT INTO usuarios (correo, password, tipo_usuario) VALUES (?, ?, ?)",
                    (usuario.correo, generate_password_hash(usuario.password), usuario.tipo_usuario),
                )
                db.session.commit()
            except IntegrityError:
                error = f"Email {usuario.correo} is already registered."

            else:
                return redirect(url_for("auth.login"))

        flash(error)

    aux = {}
    for tipos in db.session.query(TiposUsuarios).all():
        aux[tipos.id_tipo_usuario] = tipos.nombre_tipo_usuario
    return render_template('auth/register.html', tipos_usuarios=aux)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        error = None
        usuario = db.engine.execute(
            'SELECT * FROM usuarios WHERE correo = ?', (request.form['correo'],)).fetchone()
        if usuario is None:
            error = 'Invalid username or password.'
        elif not check_password_hash(usuario['password'], request.form['password']):
            error = 'Invalid username or password.'

            print(usuario['id_usuario'])
            session['id_usuario'] = usuario.id_usuario
            return render_template('stocks/index.html')
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    id_usuario = session.get('id_usuario')

    if id_usuario is None:
        g.usuario = None
    else:
        g.usuario = get_db().execute(
            'SELECT * FROM usuario WHERE id_usuario = ?', (id_usuario,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.usuario is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
