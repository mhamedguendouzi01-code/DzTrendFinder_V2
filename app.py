from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    # تأكد أن اسم الملف هو dz_finder.db
    conn = sqlite3.connect('dz_finder.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    # تأكد أن اسم الجدول هو products
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True, port=5000)