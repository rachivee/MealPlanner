# file: backend/ai_engine.py
import heapq

# --- FUNGSI BANTUAN (HELPER) ---

def group_ingredients_by_recipe(details):
    """Mengubah data SQL yang datar menjadi Dictionary per Resep"""
    mapping = {}
    for row in details:
        r_id = row['recipe_id']
        if r_id not in mapping:
            mapping[r_id] = []
        mapping[r_id].append(row)
    return mapping

def calculate_real_cost(recipe_ingredients, user_pantry):
    """
    Menghitung biaya resep.
    Jika bahan ada di pantry (user_pantry), biayanya Rp 0.
    Jika tidak, biayanya sesuai harga pasar.
    """
    cost = 0
    missing = []
    
    for item in recipe_ingredients:
        ing_name = item['name'].lower()
        if ing_name not in user_pantry:
            # Hitung harga: Harga per unit * Jumlah yang dibutuhkan
            item_cost = item['price_per_unit'] * item['amount_needed']
            cost += item_cost
            missing.append(ing_name)
            
    return cost, missing

def heuristic(current_calories, target_calories):
    """
    Fungsi Heuristik A*.
    Menghitung seberapa jauh kita dari target kalori.
    Semakin jauh selisihnya, nilai 'h' semakin besar (buruk).
    """
    diff = abs(target_calories - current_calories)
    # Kita beri bobot 10. Artinya selisih 1 kalori 'setara' denda Rp 10.
    # Ini supaya AI menyeimbangkan antara Hemat Uang vs Sehat.
    return diff * 10 

# --- ALGORITMA INTI ---

def solve_meal_plan(user_request, all_recipes, recipe_details):
    print("--- MEMULAI A* SEARCH ---")
    
    # 1. SETUP DATA
    ingredients_map = group_ingredients_by_recipe(recipe_details)
    user_pantry = [item.lower() for item in user_request.get('pantry', [])]
    user_allergies = [a.lower() for a in user_request.get('allergies', [])]
    target_cal = user_request.get('calories', 2000)
    days_needed = user_request.get('days', 1)

    # 2. FASE CSP (FILTERING)
    # Pisahkan resep jadi 3 tumpukan: Pagi, Siang, Malam
    # Sekaligus buang yang mengandung alergi
    pools = {'Breakfast': [], 'Lunch': [], 'Dinner': []}
    
    for recipe in all_recipes:
        r_id = recipe['id']
        r_ings = ingredients_map.get(r_id, [])
        
        # Cek Alergi (Constraint Satisfaction)
        is_safe = True
        for ing in r_ings:
            if ing['allergen_tag'] and ing['allergen_tag'].lower() in user_allergies:
                is_safe = False
                break
        
        if is_safe:
            # Hitung cost belanja untuk resep ini
            cost, missing = calculate_real_cost(r_ings, user_pantry)
            recipe['real_cost'] = cost
            recipe['missing'] = missing
            
            # Masukkan ke kolam yang sesuai
            m_type = recipe['meal_type']
            if m_type in pools:
                pools[m_type].append(recipe)

    # Cek apakah ada stok resep yang cukup?
    if not pools['Breakfast'] or not pools['Lunch'] or not pools['Dinner']:
        return {"error": "Maaf, tidak ada resep yang aman dari alergi Anda untuk salah satu waktu makan."}

    # 3. FASE A* SEARCH (OPTIMIZATION)
    # Kita cari kombinasi terbaik untuk setiap hari yang diminta
    final_plan = []
    
    for day in range(1, days_needed + 1):
        print(f"Mencari menu terbaik hari ke-{day}...")
        
        # Priority Queue menyimpan: (F_Score, G_Score, Current_Calories, [List Menu Terpilih])
        # Kita mulai dengan kosong
        open_set = []
        
        # Format Node: (f_score, g_cost, current_cal, path_history)
        # Push start node (kosong)
        heapq.heappush(open_set, (0, 0, 0, []))
        
        best_daily_menu = None
        
        # A* Loop: Level 1 (Pagi) -> Level 2 (Siang) -> Level 3 (Malam)
        while open_set:
            f, g, cal, path = heapq.heappop(open_set)
            
            # Kedalaman pencarian (0=Belum makan, 1=Udah Sarapan, 2=Udah Siang, 3=Selesai)
            depth = len(path)
            
            # GOAL STATE: Jika sudah pilih 3 menu (Pagi, Siang, Malam)
            if depth == 3:
                best_daily_menu = path # Karena pakai Priority Queue, yang pertama sampai pasti yang termurah (f terkecil)
                break 
            
            # Tentukan mau cari makan apa selanjutnya
            next_meal_type = ['Breakfast', 'Lunch', 'Dinner'][depth]
            candidates = pools[next_meal_type]
            
            # EXPAND NODE: Coba semua kemungkinan menu berikutnya
            for recipe in candidates:
                # Hitung G (Biaya sejauh ini + Biaya resep baru)
                new_g = g + recipe['real_cost']
                
                # Hitung Kalori baru
                new_cal = cal + recipe['total_calories']
                
                # Hitung H (Heuristik: seberapa jauh dari target kalori?)
                # Kita hitung penalti hanya kalau sudah lengkap 3 menu, atau estimasi kasar
                h = heuristic(new_cal, target_cal)
                
                # F = G + H
                new_f = new_g + h
                
                # Masukkan ke antrian untuk diperiksa
                new_path = path + [recipe]
                heapq.heappush(open_set, (new_f, new_g, new_cal, new_path))
        
        if best_daily_menu:
            # Susun data untuk dikirim ke JSON
            bf, ln, dn = best_daily_menu[0], best_daily_menu[1], best_daily_menu[2]
            
            day_result = {
                "day": day,
                "breakfast": format_output(bf),
                "lunch": format_output(ln),
                "dinner": format_output(dn),
                "total_calories": bf['total_calories'] + ln['total_calories'] + dn['total_calories'],
                "estimated_cost": bf['real_cost'] + ln['real_cost'] + dn['real_cost']
            }
            final_plan.append(day_result)

    return final_plan

def format_output(recipe):
    """Merapikan output agar enak dibaca Frontend"""
    return {
        "name": recipe['name'],
        "calories": recipe['total_calories'],
        "calculated_cost": recipe['real_cost'],
        "missing_ingredients": recipe['missing']
    }