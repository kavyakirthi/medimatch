import sqlite3

def list_events():
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Event_ID, Date, Location FROM Medical_Event')
    events = cursor.fetchall()
    conn.close()
    for e in events:
        print(f"Event ID: {e[0]} | Date: {e[1]} | Location: {e[2]}")

def create_patient():
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()
    name = input("Name: ")
    dob = input("DOB (YYYY-MM-DD): ")
    phone = input("Phone: ")
    email = input("Email: ")
    city = input("City: ")
    cursor.execute('INSERT INTO Patient (Name, DOB, Phone, Email, City) VALUES (?, ?, ?, ?, ?)',
                   (name, dob, phone, email, city))
    conn.commit()
    conn.close()
    print("✅ Patient created.")

def list_patients():
    conn = sqlite3.connect('medimatch.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Patient_ID, Name, Email, City FROM Patient')
    patients = cursor.fetchall()
    conn.close()
    print("\nRegistered Patients:")
    for p in patients:
        print(f"ID: {p[0]} | Name: {p[1]} | Email: {p[2]} | City: {p[3]}")

def main():
    while True:
        print("\nOptions:\n1. List Events\n2. Register Patient\n3. Exit\n4. List Patients")
        choice = input("Choose (1/2/3/4): ")
        if choice == '1':
            list_events()
        elif choice == '2':
            create_patient()
        elif choice == '3':
            print("Goodbye!")
            break
        elif choice == '4':
            list_patients()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
