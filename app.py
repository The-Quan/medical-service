from flask import Flask, jsonify, request
import mysql.connector
from datetime import date

app = Flask(__name__)

# Kết nối với cơ sở dữ liệu MySQL
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="medical_service"
        )
        return connection
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
        return None

# Thêm bệnh nhân
@app.route('/patients', methods=['POST'])
def add_patients():
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Không thể kết nối cơ sở dữ liệu"}), 500
    
    data = request.json
    name = data.get('name')
    birthday = data.get('birthday')
    gender = data.get('gender')
    address = data.get('address')

    cursor = connection.cursor()
    query = "INSERT INTO patients (name, birthday, gender, address) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, birthday, gender, address))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Đã thêm bệnh nhân"}), 201

# Thêm bác sĩ
@app.route('/doctors', methods=['POST'])
def add_doctors():
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Không thể kết nối cơ sở dữ liệu"}), 500

    data = request.json
    name = data.get('name')

    cursor = connection.cursor()
    query = "INSERT INTO doctors (name) VALUES (%s)"
    cursor.execute(query, (name,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Đã thêm bác sĩ"}), 201

# Thêm lịch hẹn
@app.route('/appointments', methods=['POST'])
def add_appointments():
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Không thể kết nối cơ sở dữ liệu"}), 500

    data = request.json
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    reason = data.get('reason')
    appointment_date = data.get('appointment_date')
    status = data.get('status')
    note = data.get('note')

    cursor = connection.cursor()
    query = "INSERT INTO appointments (patient_id, doctor_id, reason, appointment_date, status, note) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (patient_id, doctor_id, reason, appointment_date, status, note))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Đã thêm lịch hẹn"}), 201

# Hiển thị tất cả lịch hẹn
@app.route('/appointments', methods=['GET'])
def get_all_appointments():
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Không thể kết nối cơ sở dữ liệu"}), 500

    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT p.name AS patient_name, p.birthday, p.gender, p.address, d.name AS doctor_name, a.reason, a.appointment_date
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors d ON a.doctor_id = d.id
    """
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(results), 200

# Hiển thị lịch hẹn hôm nay
@app.route('/appointments/today', methods=['GET'])
def get_today_appointments():
    connection = connect_to_database()
    if not connection:
        return jsonify({"error": "Không thể kết nối cơ sở dữ liệu"}), 500

    today = date.today()

    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT p.address, p.name AS patient_name, p.birthday, p.gender, d.name AS doctor_name, a.status, a.note
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors d ON a.doctor_id = d.id
    WHERE a.appointment_date = %s
    """
    cursor.execute(query, (today,))
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(results), 200

# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True)
