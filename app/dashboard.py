import datetime
from os import error
import sqlite3
import flask
from flask.helpers import flash, url_for
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from app.db import get_db
from flask import (
    Blueprint, render_template, redirect,session
)
from flask.globals import request
from app.auth import admin_required,patient_required,doctor_required,technician_required,login_required
import time

bp = Blueprint('dashboard', __name__)


def render_table(title,Entity):
    
    return


@bp.route('/patient',methods=('GET', 'POST'))
@login_required
@patient_required
def patient():
    type=None
    rows=None
    
    if request.method == "POST":
        user_id = session.get("user_id")
        type = request.form['type']
        db = get_db()
        
        if type == 'scans':
            rows = db.execute(
                """SELECT id, type, time from scan
                WHERE patient_id=?
                """
            ,(user_id,)).fetchall()
        elif type == 'treatments':
            rows = db.execute(
                """SELECT medical_check.id,doctor.first_name,doctor.last_name,diagnosis,treatment
                FROM medical_check
                JOIN doctor on medical_check.doctor_id=doctor.id
                WHERE patient_id=? AND treatment IS NOT NULL
                """
            ,(user_id,)).fetchall()

    return render_template('patient.html',type=type,Entity=rows)

@bp.route('/doctor',methods=('GET', 'POST'))
@login_required
@doctor_required
def doctor():
    rows = None
    if request.method == 'POST':
        try:
            db = get_db()
            doctor_id = session.get('user_id')
            rows = db.execute(
            """SELECT  medical_check.id, patient.first_name,patient.last_name,patient.birth_date,patient.gender,patient.medical_history,
            diagnosis,treatment
            FROM medical_check
            JOIN patient on medical_check.patient_id=patient.id
            WHERE doctor_id=? AND treatment IS NULL
            """,(doctor_id,)).fetchall()
        except Exception as e:
            print(e)
            flash(e)

    return render_template('doctor.html',Entity=rows)

@bp.route('/doctor/treatment',methods=['POST'])
@login_required
@doctor_required
def treatments():
    try:
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        medical_check_id = request.form['medical-check-id']
        print(medical_check_id)
        print(diagnosis)
        print(treatment)
        db = get_db()
        db.execute(
            """UPDATE medical_check
            SET diagnosis=?, treatment=?
            WHERE id=?
            """,(diagnosis,treatment,medical_check_id))
        db.commit()
    except Exception as e:
        print(e)
        flash(e)

    return redirect(url_for('dashboard.doctor'))


@bp.route('/admin',methods=('GET', 'POST'))
@login_required
@admin_required
def admin():
    role=None
    rows=None
    stats = None
    db = get_db()
    if request.method == 'POST':
        try:
        
            role = request.form['role']
            if role == 'admins':
                rows = db.execute(
                    "SELECT first_name,last_name,phone,username,gender FROM Admin"
                ).fetchall()
            elif role == 'patients':
                rows = db.execute(
                    "SELECT first_name,last_name,phone,username,gender,birth_date,medical_history FROM Patient"
                ).fetchall()
            elif role == 'doctors':
                rows = db.execute(
                    "SELECT first_name,last_name,phone,username,gender FROM Doctor"
                ).fetchall()
            elif role == 'technicians':
                rows = db.execute(
                    "SELECT first_name,last_name,phone,username,gender FROM Technician"
                ).fetchall()
        except Exception as e:
            print(e)
            flash(e)
    else:
        try:
            stats=db.execute("""
                SELECT (
                    SELECT COUNT(*) FROM scan
                    ) as scans_count
                    ,(
                    SELECT COUNT(*) FROM doctor
                    ) as doctors_count
                    ,(
                    SELECT COUNT(*) FROM patient
                    ) as patients_count
                    ,(
                    SELECT COUNT(*) FROM technician
                    ) as technicians_count
            """).fetchone()
        except Exception as e:
            print(e)
            flash(e)
    
    return render_template('admin.html', stats=stats,role=role,Entity=rows)


@bp.route('/admin/signup',methods=('GET', 'POST'))
@login_required
@admin_required
def signup():
    if request.method == 'POST':
        try:
            first_name = request.form['first-name']
            last_name = request.form['last-name']
            phone = request.form['phone']
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm-password']
            gender = request.form['gender']
            role = request.form['role']
            admin_id = session.get('user_id')
            
            db = get_db()
            if password != confirm_password:
                raise Exception("Passwords don't match")
            
            if role == 'Admin':
                
                if db.execute(
                    'SELECT id FROM Admin WHERE username = ?', (username,)
                ).fetchone() is not None:
                 
                    raise Exception('Admin {} is already registered.'.format(username))
                
                values = (first_name,last_name,phone,username,password,gender)
                db.execute(
                        'INSERT INTO Admin (first_name,last_name,phone,username,password,gender) VALUES (?, ?,?,?,?,?)',
                        values
                    )
                db.commit()
                
            elif role == 'Patient':
                birth_date = request.form['birth-date']
                medical_history = request.form['medical-history']
                if db.execute(
                    'SELECT id FROM Patient WHERE username = ?', (username,)
                ).fetchone() is not None:
                
                    raise Exception('Patient {} is already registered.'.format(username))
                
                values = (first_name,last_name,phone,username,password,gender,birth_date,medical_history)
                db.execute(
                        'INSERT INTO Patient (first_name,last_name,phone,username,password,gender,birth_date,medical_history) VALUES (?, ?,?,?,?,?,?,?)',
                        values
                    )

                db.commit()
            
            elif role == 'Doctor':

                if db.execute(
                    'SELECT id FROM Doctor WHERE username = ?', (username,)
                ).fetchone() is not None:
                
                    raise Exception('Doctor {} is already registered.'.format(username))
                
                values = (first_name,last_name,phone,username,password,gender,admin_id)
                db.execute(
                        'INSERT INTO Doctor (first_name,last_name,phone,username,password,gender,admin_id) VALUES (?, ?,?,?,?,?,?)',
                        values
                    )
                db.commit()
            elif role == 'Technician':
                
                if db.execute(
                    'SELECT id FROM Technician WHERE username = ?', (username,)
                ).fetchone() is not None:
                
                    raise Exception('Technician {} is already registered.'.format(username))
                
                values = (first_name,last_name,phone,username,password,gender,admin_id)
                db.execute(
                        'INSERT INTO Technician (first_name,last_name,phone,username,password,gender,admin_id) VALUES (?, ?,?,?,?,?,?)',
                        values
                    )
                db.commit()
            flash("Success")
        except Exception as e:
            print(e)
            flash(e)

    return render_template('signup.html')


@bp.route('/admin/assignments',methods=('GET', 'POST'))
@login_required
@admin_required
def assignments():
    error = None
    if request.method == "POST":
        try:
            doctor_id = request.form['doctor-id']
            patient_id = request.form['patient-id']
            db=get_db()
            db.execute("INSERT INTO medical_check (patient_id,doctor_id) VALUES (?,?)",(patient_id,doctor_id,))
            db.commit()
        except Exception as e:
            print(e)
            error = e
        
        flash(error or "Success")
    
    return render_template("assignments.html")



@bp.route('/technician',methods=('GET','POST'))
@login_required
@technician_required
def technician():
    if request.method == "POST":
        try:
            user_id = session.get("user_id")
            db = get_db()
            rows = db.execute('SELECT id,type,time FROM Scan WHERE technician_id=?',(user_id,)).fetchall()
            db.commit()
            return render_template('technician.html', Entity=rows)
        except Exception as e:
            print(e)
    return render_template('technician.html')



@bp.route('/technician/upload',methods=['POST'])
@login_required
@technician_required
def upload_file():

    error = None
    try:
        db=get_db()
        file = request.files['file']
        technician_id = session.get('user_id')
        scan_type = request.form['scan-type']
        patient_id = request.form['patient-id']
        db.execute("""INSERT INTO Scan (type,patient_id,technician_id,file,time) VALUES (?,?,?,?,?)""",
        (scan_type,patient_id,technician_id,sqlite3.Binary(file.read()),time.asctime(time.localtime(time.time()))))
        db.commit()
    except Exception as e:
        print(e)
        error = e
        flash(e)
    finally:
        flash(error or "Success")
        return redirect(url_for('dashboard.technician'))
    





# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

@bp.route('/doctor/authorize',methods=['GET'])
@login_required
@doctor_required
def authorize():
    
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)
    

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for('dashboard.oauthcallback', _external=True)

    authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

    print(state)
    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


    
def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}




@bp.route('/doctor/calendar',methods=['GET'])
@login_required
@doctor_required
def oauthcallback():

    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('dashboard.oauthcallback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('dashboard.calendar'))

@bp.route('/doctor/events',methods=['GET'])
@login_required
@doctor_required
def calendar():
    if 'credentials' not in flask.session:
        return flask.redirect(url_for('dashboard.authorize'))

  # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])

    calendar = googleapiclient.discovery.build(
      'calendar', 'v3', credentials=credentials)
    
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = calendar.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    parsed_events = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        date_split = start.split('T')
        parsed_events.append({
            "date": date_split[0],
            "time": date_split[1],
            "summary": event["summary"]
        })
    
    return render_template('calendar.html',events=parsed_events)
