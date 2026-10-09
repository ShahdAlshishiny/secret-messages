import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # يسمح للفرونت إند يتواصل مع الباك إند

# بيانات الاتصال بقاعدة البيانات PostgreSQL
DB_HOST = "localhost"
DB_NAME = "my_messages_db"
DB_USER = "postgres"
DB_PASSWORD = "1234"  # 👈 غيري الكلمة دي للباسورد بتاعتك في pgAdmin
DB_PORT = "5432"

def get_db_connection():
    # هنا بيحصل الربط الفعلي بين الباك إند والداتابيز!
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

@app.route('/api/send-message', methods=['POST'])
def receive_message():
    data = request.get_json()
    name = data.get('name', 'مجهول')
    message = data.get('message', '')

    if not message.strip():
        return jsonify({'status': 'error', 'message': 'الرسالة فارغة'}), 400

    try:
        # 1. الاتصال بالداتابيز
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 2. حفظ الرسالة في جدول messages
        query = "INSERT INTO messages (name, message) VALUES (%s, %s);"
        cursor.execute(query, (name, message))
        
        # 3. تأكيد الحفظ وإغلاق الاتصال
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'تم إرسال الرسالة  !'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)