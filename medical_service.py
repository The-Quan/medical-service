import mysql.connector
import datetime

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Địa chỉ MySQL
            user="root",       # Tên người dùng MySQL
            password="",       # Mật khẩu MySQL
            database="medical_service"
        )
        print("Kết nối tới cơ sở dữ liệu thành công.")
        return connection
    except mysql.connector.Error as err:
        print(f"Lỗi kết nối cơ sở dữ liệu: {err}")
        return None

# Thêm bệnh nhân vào cơ sở dữ liệu
def add_patient(cursor, name, birthday, gender, address):
    try:
        query = "INSERT INTO patients (name, birthday, gender, address) VALUES (%s, %s, %s, %s)"
        data = (name, birthday, gender, address)
        cursor.execute(query, data)
        print(f"Thêm bệnh nhân: {name}")
    except mysql.connector.Error as err:
        print(f"Lỗi khi thêm bệnh nhân: {err}")

# Thêm bác sĩ vào cơ sở dữ liệu
def add_doctor(cursor, name):
    try:
        query = "INSERT INTO doctors (name) VALUES (%s)"
        cursor.execute(query, (name,))
        print(f"Thêm bác sĩ: {name}")
    except mysql.connector.Error as err:
        print(f"Lỗi khi thêm bác sĩ: {err}")

# Thêm cuộc hẹn vào cơ sở dữ liệu
def add_appointment(cursor, patient_id, doctor_id, reason, appointment_date, status="Pending", note=""):
    try:
        query = "INSERT INTO appointments (patient_id, doctor_id, reason, appointment_date, status, note) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (patient_id, doctor_id, reason, appointment_date, status, note)
        cursor.execute(query, data)
        print(f"Thêm cuộc hẹn cho bệnh nhân ID: {patient_id}")
    except mysql.connector.Error as err:
        print(f"Lỗi khi thêm cuộc hẹn: {err}")

# Tạo báo cáo từ cơ sở dữ liệu và in ra màn hình
def generate_report(cursor):
    try:
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
    except mysql.connector.Error as err:
        print(f"Lỗi khi tạo báo cáo: {err}")

# Hiển thị các cuộc hẹn trong ngày hôm nay
def show_today_appointments(cursor):
    try:
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
    except mysql.connector.Error as err:
        print(f"Lỗi khi hiển thị cuộc hẹn: {err}")

# Thực thi chương trình
def main():
    connection = connect_to_database()
    if connection is None:
        print("Không thể kết nối cơ sở dữ liệu. Thoát chương trình.")
        return
    
    cursor = connection.cursor()

    # Thêm dữ liệu mẫu cho bệnh nhân
    print("Thêm bệnh nhân...")
    add_patient(cursor, "Nguyen A", 2010, "Male", "Ha noi")
    add_patient(cursor, "Nguyen B", 1990, "Female", "Ha noi")
    add_patient(cursor, "Nguyen C", 1995, "Male", "Da Nang")
    print("Bệnh nhân đã được thêm.")

    # Thêm dữ liệu mẫu cho bác sĩ
    print("Thêm bác sĩ...")
    add_doctor(cursor, "Nguyen Si")
    add_doctor(cursor, "Tran Binh")
    add_doctor(cursor, "Le Quang")
    add_doctor(cursor, "Pham Hoang")
    add_doctor(cursor, "Bui Hieu")
    print("Bác sĩ đã được thêm.")

    # Thêm các cuộc hẹn mẫu
    print("Thêm cuộc hẹn...")
    add_appointment(cursor, 1, 1, "General Checkup", "2024-10-19", "Pending", "")
    add_appointment(cursor, 2, 2, "Consultation", "2024-10-19", "Done", "")
    add_appointment(cursor, 3, 3, "Routine Check", "2024-10-19", "Pending", "")
    print("Cuộc hẹn đã được thêm.")

    # Tạo báo cáo
    generate_report(cursor)

    # Hiển thị các cuộc hẹn trong ngày hôm nay
    show_today_appointments(cursor)

    # Lưu thay đổi vào cơ sở dữ liệu
    try:
        connection.commit()
        print("Dữ liệu đã được lưu vào cơ sở dữ liệu.")
    except mysql.connector.Error as err:
        print(f"Lỗi khi lưu dữ liệu: {err}")

    # Đóng kết nối
    cursor.close()
    connection.close()
    print("Kết nối đã được đóng.")

if __name__ == "__main__":
    main()
