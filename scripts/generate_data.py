from faker import Faker
import sqlite3
import random

fake = Faker()
conn = sqlite3.connect('medimatch.db')
cursor = conn.cursor()

# Create sample clinics (40)
for _ in range(40):
    cursor.execute('INSERT INTO Clinic (Name, Address) VALUES (?, ?)', 
                   (fake.company(), fake.address()))

# Create sample services (60)
services = []
for i in range(60):
    services.append((
        f"{fake.word().capitalize()} Service {i+1}",
        fake.sentence(nb_words=5)
    ))

for s in services:
    cursor.execute('INSERT INTO Service (Name, Description) VALUES (?, ?)', s)

# Create sample patients (1,000)
for i in range(1000):
    unique_email = f"user{i}@example.com"
    cursor.execute('INSERT INTO Patient (Name, DOB, Phone, Email, City) VALUES (?, ?, ?, ?, ?)',
                   (fake.name(),
                    fake.date_of_birth(minimum_age=18, maximum_age=90),
                    fake.phone_number(),
                    unique_email,
                    fake.city()))


# Create sample doctors (200)
for _ in range(200):
    cursor.execute('INSERT INTO Doctor (Name, Speciality, License_No) VALUES (?, ?, ?)',
                   (fake.name(),
                    random.choice(['Dentist', 'Ophthalmologist', 'Cardiologist', 'Therapist', 'General Practitioner']),
                    fake.bothify(text='????-#####')))

# Create sample volunteers (200)
for _ in range(200):
    cursor.execute('INSERT INTO Volunteer (Name, Role) VALUES (?, ?)',
                   (fake.name(),
                    random.choice(['Reception', 'Assistance', 'Logistics', 'Scheduling', 'Outreach'])))

# Create sample medical events (100)
for _ in range(100):
    clinic_id = random.randint(1, 40)
    cursor.execute('INSERT INTO Medical_Event (Date, Location, Clinic_ID) VALUES (?, ?, ?)',
                   (fake.date_between(start_date='-60d', end_date='+60d'),
                    fake.city(),
                    clinic_id))

# Create sample appointments (2,000)
for _ in range(2000):
    patient_id = random.randint(1, 1000)
    clinic_id = random.randint(1, 40)
    service_id = random.randint(1, 60)
    cursor.execute('INSERT INTO Appointment (Date, Status, Patient_ID, Clinic_ID, Service_ID) VALUES (?, ?, ?, ?, ?)',
                   (fake.date_between(start_date='-30d', end_date='+30d'),
                    random.choice(['confirmed', 'cancelled']),
                    patient_id,
                    clinic_id,
                    service_id))

# Create sample feedback (400)
for _ in range(400):
    patient_id = random.randint(1, 1000)
    event_id = random.randint(1, 100)
    cursor.execute('INSERT INTO Feedback (Rating, Comments, Patient_ID, Event_ID) VALUES (?, ?, ?, ?)',
                   (random.randint(1,5),
                    fake.sentence(nb_words=10),
                    patient_id,
                    event_id))

conn.commit()
conn.close()

print("✅ Large sample data generated successfully.")
