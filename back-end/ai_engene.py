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
    cost = 0
    missing = []
    for item in recipe_ingredients:
        ing_name = item['name'].lower()
        if ing_name not in user_pantry:
            item_cost = item['price_per_unit'] * item['amount_needed']
            cost += item_cost
            missing.append(ing_name)
    return cost, missing

def heuristic(current_calories, target_calories):
    # Penalti jika kalori melenceng dari target
    return abs(target_calories - current_calories) * 5

def format_output(recipe):
    return {
        "name": recipe['name'],
        "calories": recipe['total_calories'],
        "calculated_cost": recipe['real_cost'],
        "missing_ingredients": recipe['missing']
    }

# --- ALGORITMA INTI ---
def solve_meal_plan(user_request, all_recipes, recipe_details):
    print("--- MEMULAI A* SEARCH (DENGAN VARIASI & BUDGET) ---")
    
    ingredients_map = group_ingredients_by_recipe(recipe_details)
    user_pantry = [item.lower() for item in user_request.get('pantry', [])]
    user_allergies = [a.lower() for a in user_request.get('allergies', [])]
    target_cal = user_request.get('calories', 2000)
    days_needed = user_request.get('days', 1)
    
    # Ambil Budget
    total_budget = float(user_request.get('budget', 99999999)) 
    daily_budget_limit = total_budget / days_needed 

    # 1. FASE CSP (FILTERING)
    pools = {'Breakfast': [], 'Lunch': [], 'Dinner': []}
    
    for recipe in all_recipes:
        r_id = recipe['id']
        r_ings = ingredients_map.get(r_id, [])
        
        # Cek Alergi
        is_safe = True
        for ing in r_ings:
            if ing['allergen_tag'] and ing['allergen_tag'].lower() in user_allergies:
                is_safe = False
                break
        
        if is_safe:
            cost, missing = calculate_real_cost(r_ings, user_pantry)
            recipe['real_cost'] = cost
            recipe['missing'] = missing
            
            # Pruning Awal: Buang jika harga > budget harian
            if cost <= daily_budget_limit:
                if recipe['meal_type'] in pools:
                    pools[recipe['meal_type']].append(recipe)

    if not pools['Breakfast'] or not pools['Lunch'] or not pools['Dinner']:
        return {"error": "Resep tidak cukup atau budget terlalu rendah."}

    # 2. FASE A* SEARCH (OPTIMIZATION)
    final_plan = []
    
    # LIST UNTUK MENCATAT MENU HARI SEBELUMNYA (Agar tidak berulang)
    previous_day_ids = set() 
    
    for day in range(1, days_needed + 1):
        open_set = []
        # (F_Score, G_Cost, Calories, Path)
        heapq.heappush(open_set, (0, 0, 0, []))
        
        best_daily_menu = None
        
        while open_set:
            f, g, cal, path = heapq.heappop(open_set)
            
            depth = len(path)
            
            # GOAL STATE: Sudah pilih 3 menu (Pagi, Siang, Malam)
            if depth == 3:
                best_daily_menu = path
                break 
            
            next_type = ['Breakfast', 'Lunch', 'Dinner'][depth]
            candidates = pools[next_type]
            
            for recipe in candidates:
                # Hitung Biaya Uang (G)
                new_g = g + recipe['real_cost']
                
                # Cek Budget (Hard Constraint)
                if new_g > daily_budget_limit:
                    continue 

                # --- FITUR BARU: VARIETY PENALTY ---
                # Jika resep ini ADA di menu hari kemarin, beri skor buruk (Penalty)
                # Kita tidak melarang (bukan continue), tapi kita persulit agar tidak dipilih
                variety_penalty = 0
                if recipe['id'] in previous_day_ids:
                    variety_penalty = 5000 # Poin penalti sangat besar
                
                # Juga cek agar dalam SATU HARI tidak makan menu yang sama (Pagi Nasi Goreng, Siang Nasi Goreng)
                current_day_ids = [r['id'] for r in path]
                if recipe['id'] in current_day_ids:
                    variety_penalty += 10000 # Penalti lebih besar lagi

                # Hitung Total Skor (F)
                new_cal = cal + recipe['total_calories']
                h = heuristic(new_cal, target_cal)
                
                # F = Biaya Uang + Heuristik Kalori + Penalti Kebosanan
                new_f = new_g + h + variety_penalty
                
                new_path = path + [recipe]
                heapq.heappush(open_set, (new_f, new_g, new_cal, new_path))
        
        if best_daily_menu:
            # Simpan ID menu hari ini untuk dicek besok (Reset previous_day_ids)
            previous_day_ids = {r['id'] for r in best_daily_menu}
            
            final_plan.append({
                "day": day,
                "breakfast": format_output(best_daily_menu[0]),
                "lunch": format_output(best_daily_menu[1]),
                "dinner": format_output(best_daily_menu[2]),
                "total_calories": sum(r['total_calories'] for r in best_daily_menu),
                "estimated_cost": sum(r['real_cost'] for r in best_daily_menu)
            })
        else:
            return {"error": f"Gagal menyusun menu hari ke-{day}. Budget terlalu ketat."}

    return final_plan