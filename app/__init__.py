
from app.db import get_db
from flask.globals import request
from flask.helpers import flash, url_for
import os
from flask import Flask,render_template

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    from . import db
    db.init_app(app)

    from . import dashboard
    from . import auth

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    
    @app.route('/')
    def index():
        return render_template('home.html')
    
    @app.route('/contact',methods=('GET','POST'))
    def contact():
        if request.method == 'POST':
            try:
                name = request.form['full-name']
                email = request.form['email']
                message = request.form['message']
                db = get_db()
                db.execute(
                """INSERT INTO contact_message (name,email,message)
                VALUES (?,?,?)
                """,(name,email,message))
                flash('Thanks for reaching out')
            except Exception as e:
                print(e)
                flash(e)
            
        return render_template('contact-us.html')
     
    
    return app