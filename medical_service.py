import mysql.connector
import datetime

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_database():
    connection = mysql.connector.connect(
        host="localhost",  # Đúng là chỉ cần 'localhost'
        port=3306,         # Cổng mặc định 3306, thêm vào nếu cần
        user="root",       # Đổi thành user của bạn
        password="password",  # Đổi thành password của bạn
        database="medical_service"
    )
    return connection


# Thêm bệnh nhân vào cơ sở dữ liệu
def add_patient(cursor, name, birthday, gender, address):
    query = "INSERT INTO patients (name, birthday, gender, address) VALUES (%s, %s, %s, %s)"
    data = (name, birthday, gender, address)
    cursor.execute(query, data)

# Thêm bác sĩ vào cơ sở dữ liệu
def add_doctor(cursor, name):
    query = "INSERT INTO doctors (name) VALUES (%s)"
    cursor.execute(query, (name,))

# Thêm cuộc hẹn vào cơ sở dữ liệu
def add_appointment(cursor, patient_id, doctor_id, reason, appointment_date, status="Pending", note=""):
    query = "INSERT INTO appointments (patient_id, doctor_id, reason, appointment_date, status, note) VALUES (%s, %s, %s, %s, %s, %s)"
    data = (patient_id, doctor_id, reason, appointment_date, status, note)
    cursor.execute(query, data)

# Tạo báo cáo từ cơ sở dữ liệu và in ra màn hình
def generate_report(cursor):
    query = """
    SELECT patients.name, patients.birthday, patients.gender, patients.address, 
           doctors.name, appointments.reason, appointments.appointment_date
    FROM appointments
    JOIN patients ON appointments.patient_id = patients.id
    JOIN doctors ON appointments.doctor_id = doctors.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("No\tPatient name\tBirthday\tGender\tAddress\tDoctor name\tReason\tDate")
    for i, row in enumerate(results, start=1):
        print(f"{i}\t{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}")

# Hiển thị các cuộc hẹn trong ngày hôm nay
def show_today_appointments(cursor):
    today = datetime.date.today()
    query = """
    SELECT patients.name, patients.birthday, patients.gender, 
           doctors.name, appointments.status, appointments.note
    FROM appointments
    JOIN patients ON appointments.patient_id = patients.id
    JOIN doctors ON appointments.doctor_id = doctors.id
    WHERE appointments.appointment_date = %s
    """
    cursor.execute(query, (today,))
    results = cursor.fetchall()
    
    print(f"\nAppointments for today ({today}):")
    print("Address\tNo\tPatient name\tBirthday\tGender\tDoctor name\tStatus\tNote")
    for i, row in enumerate(results, start=1):
        print(f"Ha noi\t{i}\t{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}")

# Thực thi chương trình
def main():
    connection = connect_to_database()
    cursor = connection.cursor()

    # Thêm dữ liệu mẫu cho bệnh nhân
    add_patient(cursor, "Nguyen A", 2010, "Male", "Ha noi")
    add_patient(cursor, "Nguyen B", 1990, "Female", "Ha noi")
    add_patient(cursor, "Nguyen C", 1995, "Male", "Da Nang")
    
    # Thêm dữ liệu mẫu cho bác sĩ
    add_doctor(cursor, "Nguyen Si")
    add_doctor(cursor, "Tran Binh")
    add_doctor(cursor, "Le Quang")
    add_doctor(cursor, "Pham Hoang")
    add_doctor(cursor, "Bui Hieu")

    # Thêm các cuộc hẹn mẫu
    add_appointment(cursor, 1, 1, "General Checkup", "2024-10-19", "Pending", "")
    add_appointment(cursor, 2, 2, "Consultation", "2024-10-19", "Done", "")
    add_appointment(cursor, 3, 3, "Routine Check", "2024-10-19", "Pending", "")

    # Tạo báo cáo
    generate_report(cursor)

    # Hiển thị các cuộc hẹn trong ngày hôm nay
    show_today_appointments(cursor)

    # Lưu thay đổi vào cơ sở dữ liệu
    connection.commit()

    # Đóng kết nối
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
