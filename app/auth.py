import functools
from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for
)
from flask.helpers import flash
from app.db import get_db

bp = Blueprint('auth', __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(*args, **kwargs)
    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user["role"] == 'admin':
            return view(*args, **kwargs)
        else:
            return redirect(url_for('dashboard.{}'.format(g.user["role"])))
    return wrapped_view


def doctor_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user["role"] == 'doctor':
            return view(**kwargs)
        else:
            return redirect(url_for('dashboard.{}'.format(g.user["role"])))
    return wrapped_view


def technician_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user["role"] == 'technician':
            return view(**kwargs)
        else:
            return redirect(url_for('dashboard.{}'.format(g.user["role"])))
    return wrapped_view


def patient_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user["role"] == 'patient':
            return view(**kwargs)
        else:
            return redirect(url_for('dashboard.{}'.format(g.user["role"])))
    return wrapped_view



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            role = request.form['role'].lower()
            db = get_db()
            error = None
            user = None
            
            if role == 'admin':

                user = db.execute(
                    'SELECT * FROM Admin WHERE username = ?', (username,)
                ).fetchone()
            
            elif role == 'doctor':

                user = db.execute(
                    'SELECT * FROM Doctor WHERE username = ?', (username,)
                ).fetchone()

            elif role == 'patient':

                user = db.execute(
                    'SELECT * FROM Patient WHERE username = ?', (username,)
                ).fetchone()

            elif role == 'technician':

                user = db.execute(
                    'SELECT * FROM Technician WHERE username = ?', (username,)
                ).fetchone()
            
            if user is None:
                error = 'Incorrect username.'
            elif user['password'] != password:
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                session['user_role'] = role
                session['user_first_name'] = user['first_name']
                return redirect(url_for('dashboard.{}'.format(role)))
        
            raise Exception(error)
        
        except Exception as e:
            print(e)
            flash(e)

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    user_role = session.get("user_role")
    user_first_name = session.get("user_first_name")
    user = None
    if user_id is None:
        g.user = user
    else:
        if user_role == 'admin':
            
            user = (
                get_db().execute("SELECT * FROM Admin WHERE id=?", (user_id,)).fetchone()
            )
        elif user_role == 'doctor':
            
            user = (
                get_db().execute("SELECT * FROM Doctor WHERE id=?", (user_id,)).fetchone()
            )
        elif user_role == 'patient':
            
            user = (
                get_db().execute("SELECT * FROM Patient WHERE id=?", (user_id,)).fetchone()
            )
        elif user_role == 'technician':
            
            user = (
                get_db().execute("SELECT * FROM Technician WHERE id=?", (user_id,)).fetchone()
            )
    if user is not None:
        g.user = {
            "id":user,
            "role":user_role,
            "first_name":user_first_name
        }


