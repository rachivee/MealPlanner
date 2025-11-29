import heapq
import random

# HELPER FUNCTIONS

def group_ingredients_by_recipe(details):
    # Mengelompokkan baris data ingredient dari database berdasarkan ID resep.
    mapping = {}
    for row in details:
        r_id = row['recipe_id']
        if r_id not in mapping:
            mapping[r_id] = []
        mapping[r_id].append(row)
    return mapping

def calculate_real_cost(recipe_ingredients, user_pantry):
    # Menghitung estimasi biaya resep.
    cost = 0.0 
    missing = []
    
    for item in recipe_ingredients:
        ing_name = item['name'].lower()
        # Jika bahan ada di pantry (pencocokan nama sebagian), biaya dianggap Rp 0.
        is_available = False
        for pantry_item in user_pantry:
            if pantry_item in ing_name: # misal: "beras" in "beras putih".
                is_available = True
                break
        
        # Jika tidak ada, masukkan ke biaya belanja.
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
    # Menghitung penalti berdasarkan selisih kalori saat ini dengan target (Fungsi Heuristik untuk Algoritma A*).
    return abs(target_calories - current_calories) * 2

def format_output(recipe):
    # Format data resep untuk dikirim kembali ke frontend.
    return {
        "name": recipe['name'],
        "calories": int(recipe['total_calories']),
        "calculated_cost": float(recipe['real_cost']),
        "missing_ingredients": recipe['missing'] 
    }

# LOGIKA UTAMA

def solve_meal_plan(user_request, all_recipes, recipe_details):
    # Fungsi utama untuk menyusun rencana makan menggunakan algoritma A*.
    print("--- MEMULAI AI ---")
    ingredients_map = group_ingredients_by_recipe(recipe_details)
    
    # 1. Parsing Input User
    user_pantry = [item.lower() for item in user_request.get('pantry', [])]

    raw_allergies = user_request.get('allergies', [])
    user_allergy_ids = set()

    # Konversi ID alergi ke integer agar aman
    try:
        for a in raw_allergies:
            user_allergy_ids.add(int(a))
    except ValueError:
        pass

    # 2. Ambil Budget & Kalori
    try:
        target_cal = int(user_request.get('calories', 2000))
        days_needed = int(user_request.get('days', 1))
        if days_needed < 1: days_needed = 1
        
        raw_budget = user_request.get('budget')
        total_budget = float(raw_budget) if raw_budget else 10000000.0
    except ValueError:
        return {"error": "Input Kalori/Budget harus berupa angka valid."}

    # 3. Filtering Resep (Constraint Satisfaction)
    pools = {'Breakfast': [], 'Lunch': [], 'Dinner': []}
    
    for recipe in all_recipes:
        r_id = recipe['id']
        r_ings = ingredients_map.get(r_id, [])
        is_safe = True
        
        # Cek kandungan alergen dalam bahan
        for ing in r_ings:
            # Ambil ID Alergi dari bahan tersebut
            ing_allergen_id = ing.get('allergen_id')
            # Jika bahan punya ID alergi, dan ID itu ada di daftar pantangan user
            if ing_allergen_id is not None:
                if int(ing_allergen_id) in user_allergy_ids:
                    is_safe = False
                    break

        # Jika aman, hitung biaya dan masukkan ke pool
        if is_safe:
            cost, missing = calculate_real_cost(r_ings, user_pantry)
            
            recipe['real_cost'] = cost
            recipe['missing'] = missing
            recipe['total_calories'] = int(recipe['total_calories'])
            
            # Filter awal berdasarkan budget total
            if cost <= total_budget:
                m_type = str(recipe['meal_type'])
                if m_type in pools:
                    pools[m_type].append(recipe)

    # Cek ketersediaan resep setelah filter
    if not pools['Breakfast'] or not pools['Lunch'] or not pools['Dinner']:
        return {"error": "Tidak ada resep yang cocok. Coba kurangi pantangan alergi."}

    # Hitung estimasi biaya minimal untuk memberi peringatan
    min_cost_bf = min((r['real_cost'] for r in pools['Breakfast']), default=0)
    min_cost_ln = min((r['real_cost'] for r in pools['Lunch']), default=0)
    min_cost_dn = min((r['real_cost'] for r in pools['Dinner']), default=0)
    
    min_daily_survival = min_cost_bf + min_cost_ln + min_cost_dn
    total_min_required = min_daily_survival * days_needed

    warnings = []
    if total_budget < total_min_required:
        warnings.append(f"Budget Rp {total_budget:,.0f} terlalu rendah. Minimal Rp {total_min_required:,.0f}.")

    # 4. Optimasi A* Search
    final_plan = []
    global_used_ids = set() 
    current_total_spent = 0.0
    
    for day in range(1, days_needed + 1):
        money_left = total_budget - current_total_spent
        days_remaining = days_needed - day
        
        # Hitung limit harian dinamis
        daily_limit = money_left - (days_remaining * min_daily_survival)
        if daily_limit < min_daily_survival:
            daily_limit = min_daily_survival

        # Inisialisasi Priority Queue A* (f_score, tie_breaker, path)
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
            random.shuffle(candidates) # Shuffle agar hasil bervariasi
            
            for recipe in candidates:
                # Hitung g(n): Biaya sejauh ini
                path_cost = sum(r['real_cost'] for r in path)
                new_g = path_cost + recipe['real_cost']
                
                # Hard Constraint: Tidak boleh melebihi budget harian
                if new_g > daily_limit:
                    continue 

                # Soft Constraint: Penalti variasi menu
                variety_penalty = 0.0
                if recipe['id'] in global_used_ids:
                    # Penalti ringan (pernah makan di hari lain)
                    variety_penalty = 2000.0 
                
                current_day_ids = [r['id'] for r in path]
                if recipe['id'] in current_day_ids:
                    # Penalti berat (makan menu sama hari ini)
                    variety_penalty += 99999.0 

                # Heuristik Kalori h(n)
                current_cal_path = sum(r['total_calories'] for r in path)
                new_cal = current_cal_path + recipe['total_calories']
                h = float(heuristic(new_cal, target_cal))
                
                # Normalisasi & Pembobotan Skor
                normalized_cost = new_g / 1000.0 
                w_cost = 1.0
                w_cal = 1.5
                
                new_f = (normalized_cost * w_cost) + variety_penalty + (h * w_cal)
                
                new_path = path + [recipe]
                heapq.heappush(open_set, (new_f, random.random(), new_path))
        
        # Simpan hasil harian jika ditemukan
        if best_daily_menu:
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