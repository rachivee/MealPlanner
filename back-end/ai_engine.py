import heapq
import random

# --- HELPER FUNCTIONS ---

def group_ingredients_by_recipe(details):
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
    Jika nama bahan ada di pantry (Partial Match), biayanya Rp 0.
    """
    cost = 0.0 
    missing = []
    
    for item in recipe_ingredients:
        ing_name = item['name'].lower()
        
        # --- LOGIKA PARTIAL MATCH (PANTRY) ---
        # Cek apakah bahan resep 'mirip' dengan yang ada di pantry
        is_available = False
        for pantry_item in user_pantry:
            if pantry_item in ing_name: # misal: "beras" in "beras putih"
                is_available = True
                break
        
        # Jika TIDAK ADA di pantry, hitung biayanya
        if not is_available:
            price = float(item['price_per_unit'])
            amount = float(item['amount_needed'])
            item_cost = price * amount
            
            cost += item_cost
            
            missing.append({
                "name": item['name'],
                "amount": amount,
                "unit": item['unit'],
                "price_per_unit": price
            })
            
    return cost, missing

def heuristic(current_calories, target_calories):
    # Selisih kalori sebagai penalti
    return abs(target_calories - current_calories) * 2

def format_output(recipe):
    return {
        "name": recipe['name'],
        "calories": int(recipe['total_calories']),
        "calculated_cost": float(recipe['real_cost']),
        "missing_ingredients": recipe['missing'] 
    }

# --- ALGORITMA INTI ---

def solve_meal_plan(user_request, all_recipes, recipe_details):
    print("--- MEMULAI AI (BASIC LOGIC + FIXED ALLERGY) ---")
    
    ingredients_map = group_ingredients_by_recipe(recipe_details)
    
    # 1. Ambil Pantry (Lowercase)
    user_pantry = [item.lower() for item in user_request.get('pantry', [])]
    
    # 2. Ambil & Validasi Alergi (FIXED LOGIC)
    # Masalah utamanya ada di sini sebelumnya: String vs Int
    raw_allergies = user_request.get('allergies', [])
    user_allergy_ids = set()
    try:
        # Kita paksa ubah setiap item jadi Integer agar cocok dengan Database
        for a in raw_allergies:
            user_allergy_ids.add(int(a))
    except ValueError:
        print("[WARNING] Ada format alergi yang salah (bukan angka), dilewati.")
    
    print(f"[DEBUG] User Allergy IDs: {user_allergy_ids}")

    # 3. Ambil Budget & Kalori
    try:
        target_cal = int(user_request.get('calories', 2000))
        days_needed = int(user_request.get('days', 1))
        if days_needed < 1: days_needed = 1
        
        raw_budget = user_request.get('budget')
        total_budget = float(raw_budget) if raw_budget else 10000000.0
    except ValueError:
        return {"error": "Input Kalori/Budget harus berupa angka valid."}

    # 4. FASE FILTERING (Constraint Satisfaction)
    pools = {'Breakfast': [], 'Lunch': [], 'Dinner': []}
    
    for recipe in all_recipes:
        r_id = recipe['id']
        r_ings = ingredients_map.get(r_id, [])
        
        is_safe = True
        
        # Cek setiap bahan dalam resep
        for ing in r_ings:
            # Ambil ID Alergi dari bahan tersebut
            ing_allergen_id = ing.get('allergen_id')
            
            # Jika bahan punya ID alergi, dan ID itu ada di daftar pantangan user
            if ing_allergen_id is not None:
                if int(ing_allergen_id) in user_allergy_ids:
                    is_safe = False
                    # print(f"[DEBUG] Skip {recipe['name']} karena mengandung allergen ID {ing_allergen_id}")
                    break
        
        if is_safe:
            # Hitung biaya jika aman
            cost, missing = calculate_real_cost(r_ings, user_pantry)
            
            recipe['real_cost'] = cost
            recipe['missing'] = missing
            recipe['total_calories'] = int(recipe['total_calories'])
            
            # Cek Budget Global (Opsional, biar tidak terlalu berat di A*)
            if cost <= total_budget:
                m_type = str(recipe['meal_type'])
                if m_type in pools:
                    pools[m_type].append(recipe)

    # Cek ketersediaan resep setelah filter
    if not pools['Breakfast'] or not pools['Lunch'] or not pools['Dinner']:
        return {"error": "Tidak ada resep yang cocok. Coba kurangi pantangan alergi."}

    # Hitung kebutuhan minimal (untuk warning)
    min_cost_bf = min((r['real_cost'] for r in pools['Breakfast']), default=0)
    min_cost_ln = min((r['real_cost'] for r in pools['Lunch']), default=0)
    min_cost_dn = min((r['real_cost'] for r in pools['Dinner']), default=0)
    
    min_daily_survival = min_cost_bf + min_cost_ln + min_cost_dn
    total_min_required = min_daily_survival * days_needed

    warnings = []
    if total_budget < total_min_required:
        warnings.append(f"Budget Rp {total_budget:,.0f} terlalu rendah. Minimal Rp {total_min_required:,.0f}.")

    # 5. FASE OPTIMASI A* (Logika Biasa / Basic A*)
    final_plan = []
    global_used_ids = set() 
    current_total_spent = 0.0
    
    for day in range(1, days_needed + 1):
        money_left = total_budget - current_total_spent
        days_remaining = days_needed - day
        
        # Limit harian dinamis
        daily_limit = money_left - (days_remaining * min_daily_survival)
        if daily_limit < min_daily_survival:
            daily_limit = min_daily_survival

        # Priority Queue: (f_score, tie_breaker, path)
        open_set = []
        heapq.heappush(open_set, (0.0, random.random(), []))
        
        best_daily_menu = None
        
        while open_set:
            f, _, path = heapq.heappop(open_set)
            depth = len(path)
            
            # Goal State: Sudah dapat 3 menu (Pagi, Siang, Malam)
            if depth == 3:
                best_daily_menu = path
                break 
            
            next_type = ['Breakfast', 'Lunch', 'Dinner'][depth]
            candidates = pools[next_type]
            # Shuffle agar hasil tidak monoton
            random.shuffle(candidates)
            
            for recipe in candidates:
                # Hitung g(n): Biaya sejauh ini
                path_cost = sum(r['real_cost'] for r in path)
                new_g = path_cost + recipe['real_cost']
                
                # Hard Constraint: Budget Harian
                if new_g > daily_limit:
                    continue 

                # Soft Constraint: Variasi Menu
                variety_penalty = 0.0
                if recipe['id'] in global_used_ids:
                    variety_penalty = 2000.0 # Penalti ringan (pernah makan di hari lain)
                
                current_day_ids = [r['id'] for r in path]
                if recipe['id'] in current_day_ids:
                    variety_penalty += 99999.0 # Penalti berat (makan menu sama hari ini)

                # Heuristik Kalori h(n)
                current_cal_path = sum(r['total_calories'] for r in path)
                new_cal = current_cal_path + recipe['total_calories']
                h = float(heuristic(new_cal, target_cal))
                
                # Pembobotan & Normalisasi Skala
                # Bagi harga dengan 1000 agar 1 poin ~ Rp 1.000 (sebanding dengan kalori)
                normalized_cost = new_g / 1000.0 
                
                w_cost = 1.0
                w_cal = 1.5
                
                # f(n) = g(n) + h(n)
                new_f = (normalized_cost * w_cost) + variety_penalty + (h * w_cal)
                
                new_path = path + [recipe]
                heapq.heappush(open_set, (new_f, random.random(), new_path))
        
        if best_daily_menu:
            # Simpan ID agar besok tidak monoton
            for r in best_daily_menu:
                global_used_ids.add(r['id'])
            
            day_cost = sum(float(r['real_cost']) for r in best_daily_menu)
            current_total_spent += day_cost
            total_cals = sum(int(r['total_calories']) for r in best_daily_menu)

            final_plan.append({
                "day": day,
                "breakfast": format_output(best_daily_menu[0]),
                "lunch": format_output(best_daily_menu[1]),
                "dinner": format_output(best_daily_menu[2]),
                "total_calories": total_cals,
                "estimated_cost": day_cost
            })
        else:
            return {"error": f"Gagal menyusun menu hari ke-{day}. Budget terlalu ketat."}

    return {
        "menu": final_plan,
        "warnings": warnings
    }