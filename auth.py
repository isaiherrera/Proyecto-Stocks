import functools

from bbdd.models import Usuario
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from bbdd import db
from bbdd.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    success = None
    if request.method == 'POST':
        usuario = Usuario(correo=request.form['correo'],
                          password=request.form['password'],
                          type='cliente')

        error = None

        if not usuario.correo:
            error = 'Se requiere un usuario.'
        elif not usuario.password:
            error = 'Se requiere una contraseña.'

        if error is None:
            try:
                usuario.password = generate_password_hash(usuario.password)
                db.session.add(usuario)
                db.session.commit()

            except IntegrityError:
                error = f"El correo {usuario.correo} ya está registrado."

            else:
                success = f"Se ha creado el usuario: {usuario.correo} con éxito"
                return render_template('auth/login.html', success=success)

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        error = None
        usuario = db.session.query(Usuario).filter(Usuario.correo == correo).first()
        if usuario is None:
            error = 'Usuario o contraseña incorrectos.'
        elif not check_password_hash(usuario.password, request.form['password']):
            error = 'Usuario o contraseña incorrectos.'

        if error is None:
            session.clear()
            session['id_usuario'] = usuario.id_usuario
            return redirect(url_for('index'))
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
