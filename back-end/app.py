from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_db_connection
from ai_engine import solve_meal_plan 

# Konfigurasi Aplikasi
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Endpoint API

@app.route('/allergens', methods=['GET'])
def get_allergens():
    # Endpoint untuk mengambil daftar alergi yang tersedia di database.
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM allergens")
    allergens = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(allergens)

@app.route('/generate-menu', methods=['POST'])
def generate_menu():
    # Endpoint utama untuk menghasilkan rencana makan.
    try:
        # Terima data dari frontend
        user_input = request.json 
        print(f"\n[REQUEST] User Input: {user_input}")

        # Koneksi dan ambil data dari database
        conn = get_db_connection()
        if not conn:
            print("[ERROR] Database Connection Failed")
            return jsonify({"error": "Database Error: Gagal konek MySQL"}), 500
            
        cursor = conn.cursor(dictionary=True)
        
        # Ambil semua resep
        cursor.execute("SELECT * FROM recipes")
        all_recipes = cursor.fetchall()
        
        # Ambil detail bahan & harga untuk kalkulasi
        cursor.execute("""
            SELECT 
                ri.recipe_id, 
                i.name, 
                i.price_per_unit, 
                i.unit, 
                i.allergen_id,
                ri.amount_needed
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.id
        """)
        all_recipe_details = cursor.fetchall()
        
        cursor.close()
        conn.close()

        # Jalankan AI Engine
        print("[PROCESS] Sedang menghitung menu...")
        meal_plan = solve_meal_plan(user_input, all_recipes, all_recipe_details)

        # Cek Hasil sebelum dikirim
        if isinstance(meal_plan, dict) and "error" in meal_plan:
            print(f"[RESULT] Gagal: {meal_plan['error']}")
        else:
            print(f"[RESULT] Berhasil membuat {len(meal_plan)} hari menu.")
        
        return jsonify(meal_plan)
        
    except Exception as e:
        print(f"[FATAL ERROR]: {e}")
        return jsonify({"error": "Terjadi kesalahan internal server"}), 500

if __name__ == '__main__':
    print("Server Meal Planner Berjalan di http://127.0.0.1:5000")
    app.run(debug=True, port=5000)