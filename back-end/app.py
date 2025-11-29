# file: backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_db_connection
# FIX: Import dari nama file yang sudah diperbaiki (ai_engine)
from ai_engine import solve_meal_plan 

app = Flask(__name__)
# Izinkan akses dari mana saja (mempermudah development)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/generate-menu', methods=['POST'])
def generate_menu():
    try:
        # 1. Terima Data dari Frontend
        user_input = request.json 
        print(f"\n[REQUEST] User Input: {user_input}")

        # 2. Ambil Data dari Database
        conn = get_db_connection()
        if not conn:
            print("[ERROR] Database Connection Failed")
            return jsonify({"error": "Database Error: Gagal konek MySQL"}), 500
            
        cursor = conn.cursor(dictionary=True)
        
        # Ambil Resep
        cursor.execute("SELECT * FROM recipes")
        all_recipes = cursor.fetchall()
        
        # Ambil Detail Bahan & Harga
        cursor.execute("""
            SELECT ri.recipe_id, i.name, i.price_per_unit, i.unit, i.allergen_tag, ri.amount_needed
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.id
        """)
        all_recipe_details = cursor.fetchall()
        
        cursor.close()
        conn.close()

        # 3. Jalankan AI Engine
        print("[PROCESS] Sedang menghitung menu...")
        meal_plan = solve_meal_plan(user_input, all_recipes, all_recipe_details)

        # 4. Cek Hasil sebelum dikirim
        if isinstance(meal_plan, dict) and "error" in meal_plan:
            print(f"[RESULT] Gagal: {meal_plan['error']}")
        else:
            print(f"[RESULT] Berhasil membuat {len(meal_plan)} hari menu.")
        
        return jsonify(meal_plan)
        
    except Exception as e:
        print(f"[FATAL ERROR]: {e}")
        return jsonify({"error": "Terjadi kesalahan internal server"}), 500

if __name__ == '__main__':
    print("🚀 Server Meal Planner Berjalan di http://127.0.0.1:5000")
    app.run(debug=True, port=5000)