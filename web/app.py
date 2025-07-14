
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Event_ID, Date, Location FROM Medical_Event')
    events = cursor.fetchall()
    conn.close()
    return render_template('home.html', events=events)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        phone = request.form['phone']
        email = request.form['email']
        city = request.form['city']
        conn = sqlite3.connect('medimatch.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Patient (Name, DOB, Phone, Email, City) VALUES (?, ?, ?, ?, ?)',
                       (name, dob, phone, email, city))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('register.html')

@app.route("/events")
def events():
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Event_ID, Date, Location FROM Medical_Event')
    events = cursor.fetchall()
    conn.close()
    return render_template('events.html', events=events)

@app.route("/events/register/<int:event_id>", methods=['GET', 'POST'])
def register_event(event_id):
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        cursor.execute('INSERT INTO Event_Registration (Patient_ID, Event_ID) VALUES (?, ?)',
                       (patient_id, event_id))
        conn.commit()
        conn.close()
        return redirect('/events')

    # Get all patients to choose from
    cursor.execute('SELECT Patient_ID, Name FROM Patient')
    patients = cursor.fetchall()
    conn.close()
    return render_template('register_event.html', patients=patients, event_id=event_id)

@app.route("/appointments", methods=['GET', 'POST'])
def appointments():
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()

    query = '''
        SELECT Appointment_ID, Date, Status, 
               Patient.Name, Clinic.Name, Service.Name
        FROM Appointment
        JOIN Patient ON Appointment.Patient_ID = Patient.Patient_ID
        JOIN Clinic ON Appointment.Clinic_ID = Clinic.Clinic_ID
        JOIN Service ON Appointment.Service_ID = Service.Service_ID
    '''
    params = []

    if request.method == 'POST':
        conditions = []
        date_from = request.form['date_from']
        date_to = request.form['date_to']
        status = request.form['status']

        if date_from:
            conditions.append('Date >= ?')
            params.append(date_from)
        if date_to:
            conditions.append('Date <= ?')
            params.append(date_to)
        if status and status != 'all':
            conditions.append('Status = ?')
            params.append(status)

        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

    cursor.execute(query, params)
    appointments = cursor.fetchall()
    conn.close()
    return render_template('appointments.html', appointments=appointments)

@app.route("/appointments/book", methods=['GET', 'POST'])
def book_appointment():
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        date = request.form['date']
        status = request.form['status']
        patient_id = request.form['patient_id']
        clinic_id = request.form['clinic_id']
        service_id = request.form['service_id']

        cursor.execute('''
            INSERT INTO Appointment (Date, Status, Patient_ID, Clinic_ID, Service_ID)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, status, patient_id, clinic_id, service_id))
        conn.commit()
        conn.close()
        return redirect('/appointments')

    # Get dropdown data
    cursor.execute('SELECT Patient_ID, Name FROM Patient')
    patients = cursor.fetchall()
    cursor.execute('SELECT Clinic_ID, Name FROM Clinic')
    clinics = cursor.fetchall()
    cursor.execute('SELECT Service_ID, Name FROM Service')
    services = cursor.fetchall()

    conn.close()
    return render_template('book_appointment.html',
                           patients=patients,
                           clinics=clinics,
                           services=services)

@app.route("/feedback")
def feedback():
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Feedback_ID, Rating, Comments, 
               Patient.Name, Medical_Event.Location
        FROM Feedback
        JOIN Patient ON Feedback.Patient_ID = Patient.Patient_ID
        JOIN Medical_Event ON Feedback.Event_ID = Medical_Event.Event_ID
    ''')
    feedbacks = cursor.fetchall()
    conn.close()
    return render_template('feedback.html', feedbacks=feedbacks)
@app.route("/feedback/submit", methods=['GET', 'POST'])
def submit_feedback():
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        rating = request.form['rating']
        comments = request.form['comments']
        patient_id = request.form['patient_id']
        event_id = request.form['event_id']

        cursor.execute('''
            INSERT INTO Feedback (Rating, Comments, Patient_ID, Event_ID)
            VALUES (?, ?, ?, ?)
        ''', (rating, comments, patient_id, event_id))
        conn.commit()
        conn.close()
        return redirect('/feedback')

    # Get dropdown data
    cursor.execute('SELECT Patient_ID, Name FROM Patient')
    patients = cursor.fetchall()
    cursor.execute('SELECT Event_ID, Location FROM Medical_Event')
    events = cursor.fetchall()

    conn.close()
    return render_template('submit_feedback.html',
                           patients=patients,
                           events=events)
@app.route("/patients/search", methods=['GET', 'POST'])
def search_patients():
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()
    results = []
    if request.method == 'POST':
        search_term = request.form['search']
        cursor.execute('''
            SELECT Patient_ID, Name, Email, City
            FROM Patient
            WHERE Name LIKE ?
        ''', ('%' + search_term + '%',))
        results = cursor.fetchall()
    conn.close()
    return render_template('search_patients.html', results=results)
@app.route("/events/registrations/<int:event_id>")
def event_registrations(event_id):
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()

    # Get event details
    cursor.execute('SELECT Date, Location FROM Medical_Event WHERE Event_ID = ?', (event_id,))
    event = cursor.fetchone()

    # Get registered patients
    cursor.execute('''
        SELECT Patient.Patient_ID, Patient.Name, Patient.Email, Patient.City
        FROM Event_Registration
        JOIN Patient ON Event_Registration.Patient_ID = Patient.Patient_ID
        WHERE Event_Registration.Event_ID = ?
    ''', (event_id,))
    registrations = cursor.fetchall()

    conn.close()
    return render_template('event_registrations.html',
                           event=event,
                           registrations=registrations)

if __name__ == "__main__":
    app.run(debug=True)
