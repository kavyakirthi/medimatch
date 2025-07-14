import sqlite3

conn = sqlite3.connect('medimatch.db')
cursor = conn.cursor()

# Create Patient table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Patient (
    Patient_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    DOB DATE,
    Phone TEXT UNIQUE,
    Email TEXT UNIQUE,
    City TEXT
);
''')

# Create Clinic table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Clinic (
    Clinic_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Address TEXT
);
''')

# Create Service table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Service (
    Service_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Description TEXT
);
''')

# Create Doctor table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Doctor (
    Doctor_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Speciality TEXT,
    License_No TEXT
);
''')

# Create Volunteer table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Volunteer (
    Volunteer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Role TEXT
);
''')

# Create Medical_Event table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Medical_Event (
    Event_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Date DATE,
    Location TEXT,
    Clinic_ID INTEGER,
    FOREIGN KEY (Clinic_ID) REFERENCES Clinic(Clinic_ID)
);
''')

# Create Appointment table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Appointment (
    Appointment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Date DATE,
    Status TEXT CHECK(Status IN ('confirmed', 'cancelled')),
    Patient_ID INTEGER,
    Clinic_ID INTEGER,
    Service_ID INTEGER,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Clinic_ID) REFERENCES Clinic(Clinic_ID),
    FOREIGN KEY (Service_ID) REFERENCES Service(Service_ID)
);
''')

# Create Feedback table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Feedback (
    Feedback_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Rating INTEGER,
    Comments TEXT,
    Patient_ID INTEGER,
    Event_ID INTEGER,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Event_ID) REFERENCES Medical_Event(Event_ID)
);
''')
# Create Event_Registration table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Event_Registration (
    Registration_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Patient_ID INTEGER,
    Event_ID INTEGER,
    FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY (Event_ID) REFERENCES Medical_Event(Event_ID)
);
''')


conn.commit()
conn.close()

print("Database and tables created successfully.")
