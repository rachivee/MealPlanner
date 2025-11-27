# file: backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS # Wajib ada
from database import get_db_connection
from ai_engene import solve_meal_plan

app = Flask(__name__)

# IZINKAN FRONTEND VUE MENGAKSES PYTHON
# resources={r"/*": {"origins": "*"}} artinya "Siapa saja boleh akses"
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/generate-menu', methods=['POST'])
def generate_menu():
    try:
        user_input = request.json 
        print(f"Menerima Request dari Vue: {user_input}") # Print ke terminal biar kelihatan

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database Error: Gagal konek MySQL"}), 500
            
        cursor = conn.cursor(dictionary=True)

        # 1. Ambil Data Resep
        cursor.execute("SELECT * FROM recipes")
        all_recipes = cursor.fetchall()
        
        # 2. Ambil Data Bahan
        cursor.execute("""
            SELECT ri.recipe_id, i.name, i.price_per_unit, i.unit, i.allergen_tag, ri.amount_needed
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.id
        """)
        all_recipe_details = cursor.fetchall()
        
        cursor.close()
        conn.close()

        # 3. Panggil AI
        meal_plan = solve_meal_plan(user_input, all_recipes, all_recipe_details)

        return jsonify(meal_plan)
        
    except Exception as e:
        print(f"ERROR DI SERVER: {e}") # Print error ke terminal
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)