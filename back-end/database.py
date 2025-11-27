# file: backend/database.py
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Fungsi untuk membuka koneksi ke database MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='meal_planner', # Pastikan nama database sama dengan di phpMyAdmin
            user='root',             # User default XAMPP biasanya 'root'
            password=''              # Password default XAMPP biasanya kosong
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None