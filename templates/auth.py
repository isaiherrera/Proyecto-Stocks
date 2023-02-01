import functools

from models import Usuario
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
import db
from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = Usuario(correo=request.form['correo'],
                          password=request.form['password'])
        print(usuario)
        error = None

        if not usuario.correo:
            error = 'Se requiere un usuario.'
        elif not usuario.password:
            error = 'Se requiere una contraseña.'

        if error is None:
            try:
                db.engine.execute(
                    "INSERT INTO usuario (correo, password) VALUES (?, ?)",
                    (usuario.correo, generate_password_hash(usuario.password)),
                )
                db.session.commit()
            except IntegrityError:
                error = f"El correo {usuario.correo} ya está registrado."

            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        usuario1 = Usuario(correo=request.form['correo'], password=request.form['password'])
        error = None
        usuario = db.engine.execute(
            'SELECT * FROM usuario WHERE correo = ?', (usuario1.correo,)
        ).fetchone()
        if usuario is None:
            error = 'Usuario o contraseña incorrectos.'
        elif not check_password_hash(usuario['password'], usuario1.password):
            error = 'Usuario o contraseña incorrectos.'

        if error is None:
            session.clear()
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



