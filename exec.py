import time
import os
import sqlite3
db=sqlite3.connect(os.path.join("instance","flaskr.sqlite"))

# for i in range(1,100):
#         db.execute("INSERT INTO Admin (first_name,last_name,gender,username,password) VALUES (?,?,?,?,?)",('Afirst','Alast','Male',str(i) + "@gmail.com",str(i)))
# for i in range(1,100):
#         db.execute("INSERT INTO Doctor (first_name,last_name,gender,username,password,admin_id) VALUES (?,?,?,?,?,?)",('Dfirst','Dlast','Male',str(i) + "@gmail.com",str(i),i))
# for i in range(1,100):
#         db.execute("INSERT INTO Technician (first_name,last_name,gender,username,password,admin_id) VALUES (?,?,?,?,?,?)",('Tfirst','Tlast','Male',str(i) + "@gmail.com",str(i),i))
# for i in range(1,100):
#         db.execute("INSERT INTO Patient (first_name,last_name,gender,username,password,medical_history,birth_date) VALUES (?,?,?,?,?,?,?)",('Pfirst','Plast','Male',str(i) + "@gmail.com",str(i),"healthy","2000-1-12"))
# for i in range(1,100):
#         if i % 2 == 0:
#                 scan="MRI"
#         else:
#                 scan="XRAY"
#         db.execute("INSERT INTO Scan (type,time,patient_id,technician_id) VALUES (?,?,?,?)",(scan,time.asctime( time.localtime(time.time())),str(i),str(i)))

# for i in range(1,100):
#         if i % 2 == 0:
#             db.execute("INSERT INTO 'medical_check' (patient_id,doctor_id) VALUES (?,?)",(i,100-i))
#         else:
#             db.execute("INSERT INTO 'medical_check' (patient_id,doctor_id) VALUES (?,?)",(i,100-i))

# db.commit()

# t=db.execute(
#                 "SELECT * FROM Technician"
#             ).fetchall().__len__()
# p=db.execute(
#                 "SELECT * FROM Patient"
#             ).fetchall().__len__()
# a=db.execute(
#                 "SELECT * FROM Admin"
#             ).fetchall().__len__()
# d=db.execute(
#                 "SELECT * FROM Doctor"
#             ).fetchall().__len__()
# s=db.execute(
#                 "SELECT * FROM Scan WHERE type='XRAY'"
#             ).fetchall().__len__()
db.row_factory = sqlite3.Row
# ps=db.execute(
#                 """SELECT patient_scan.scan_id, patient_scan.type, patient_scan.time from patient_scan
#                 JOIN scan on patient_scan.scan_id=scan.id
#                 JOIN patient on patient_scan.patient_id=patient.id
#                 WHERE patient.id=2
#                 """
#             ).fetchall()
# ps=db.execute(
#                 """SELECT * from patient_scan
#                 JOIN scan on patient_scan.scan_id=scan.id
#                 JOIN patient on scan.patient_id=patient.id
#                 WHERE scan.type='MRI'"""
#             ).fetchall()

# get all scans by a patient
# ps=db.execute('SELECT * FROM patient_diagnosis WHERE doctor_id=2').fetchall().__len__()
# print(ps)
# doctor_id = 1
# ps=db.execute(
#             """SELECT diagnosis,treatment,patient.first_name,patient.last_name 
#             FROM medical_check
#             JOIN patient on patient_diagnosis.patient_id=patient.id
#             WHERE doctor_id=?
#             """,(doctor_id,)).fetchall()
# for row in ps:
#     print(dict(row))
# print(ps)
# print(t==99)
# print(a==99)
# print(p==99)
# print(d==99)



# r=db.execute(
#             """SELECT patient.first_name,patient.last_name,patient.birth_date,patient.gender,patient.medical_history,
#             diagnosis,treatment 
#             FROM medical_check
#             JOIN patient on medical_check.patient_id=patient.id
#             WHERE doctor_id=?
#             """,(1,)).fetchone()
# x=db.execute("""UPDATE medical_check
#             SET diagnosis='bad', treatment='good'
#             WHERE id=1
#             """)
# r = db.execute("""SELECT * FROM medical_check WHERE id=1""").fetchone()
# print(dict(r))
# x=

# print(dict(x))
# for a in x:
#     print(dict(a))
