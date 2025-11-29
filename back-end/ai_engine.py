# file: backend/ai_engine.py
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
    cost = 0.0 
    missing = []
    
    for item in recipe_ingredients:
        ing_name = item['name'].lower()
        if ing_name not in user_pantry:
            price = float(item['price_per_unit'])
            amount = float(item['amount_needed'])
            item_cost = price * amount
            
            cost += item_cost
            
            # UPDATE: Kirim detail lengkap, bukan cuma nama
            missing.append({
                "name": item['name'],
                "amount": amount,
                "unit": item['unit'],
                "price_per_unit": price
            })
            
    return cost, missing

def heuristic(current_calories, target_calories):
    return abs(target_calories - current_calories) * 2

def format_output(recipe):
    return {
        "name": recipe['name'],
        "calories": int(recipe['total_calories']),
        "calculated_cost": float(recipe['real_cost']),
        "missing_ingredients": recipe['missing'] # Sekarang isinya list of objects
    }

# --- ALGORITMA INTI ---
def solve_meal_plan(user_request, all_recipes, recipe_details):
    print("--- MEMULAI AI (DETAILED SHOPPING LIST) ---")
    
    ingredients_map = group_ingredients_by_recipe(recipe_details)
    user_pantry = [item.lower() for item in user_request.get('pantry', [])]
    user_allergies = [a.lower() for a in user_request.get('allergies', [])]
    
    try:
        target_cal = int(user_request.get('calories', 2000))
        days_needed = int(user_request.get('days', 1))
        if days_needed < 1: days_needed = 1
        
        raw_budget = user_request.get('budget')
        total_budget = float(raw_budget) if raw_budget else 10000000.0
    except ValueError:
        return {"error": "Input harus berupa angka valid."}

    # 1. FASE FILTERING
    pools = {'Breakfast': [], 'Lunch': [], 'Dinner': []}
    
    for recipe in all_recipes:
        r_id = recipe['id']
        r_ings = ingredients_map.get(r_id, [])
        
        is_safe = True
        for ing in r_ings:
            tag = ing.get('allergen_tag')
            if tag and tag.lower() in user_allergies:
                is_safe = False
                break
        
        if is_safe:
            cost, missing = calculate_real_cost(r_ings, user_pantry)
            recipe['real_cost'] = cost
            recipe['missing'] = missing
            recipe['total_calories'] = int(recipe['total_calories'])
            
            if cost <= total_budget:
                m_type = str(recipe['meal_type'])
                if m_type in pools:
                    pools[m_type].append(recipe)

    if not pools['Breakfast'] or not pools['Lunch'] or not pools['Dinner']:
        return {"error": "Tidak ada resep yang cocok."}

    # Hitung biaya minimal
    min_cost_bf = min((r['real_cost'] for r in pools['Breakfast']), default=0)
    min_cost_ln = min((r['real_cost'] for r in pools['Lunch']), default=0)
    min_cost_dn = min((r['real_cost'] for r in pools['Dinner']), default=0)
    min_daily_survival = min_cost_bf + min_cost_ln + min_cost_dn
    total_min_required = min_daily_survival * days_needed

    warnings = []
    if total_budget < total_min_required:
        warnings.append(f"Budget Rp {total_budget:,.0f} terlalu rendah. Minimal Rp {total_min_required:,.0f}.")

    # 2. FASE OPTIMASI A*
    final_plan = []
    global_used_ids = set() 
    current_total_spent = 0.0
    
    for day in range(1, days_needed + 1):
        money_left = total_budget - current_total_spent
        days_remaining = days_needed - day
        daily_limit = money_left - (days_remaining * min_daily_survival)
        
        if daily_limit < min_daily_survival:
            daily_limit = min_daily_survival

        open_set = []
        heapq.heappush(open_set, (0.0, random.random(), []))
        
        best_daily_menu = None
        
        while open_set:
            f, _, path = heapq.heappop(open_set)
            depth = len(path)
            
            if depth == 3:
                best_daily_menu = path
                break 
            
            next_type = ['Breakfast', 'Lunch', 'Dinner'][depth]
            candidates = pools[next_type]
            random.shuffle(candidates)
            
            for recipe in candidates:
                path_cost = sum(r['real_cost'] for r in path)
                new_g = path_cost + recipe['real_cost']
                
                if new_g > daily_limit:
                    continue 

                variety_penalty = 0.0
                if recipe['id'] in global_used_ids:
                    variety_penalty = 50000000.0 
                
                current_day_ids = [r['id'] for r in path]
                if recipe['id'] in current_day_ids:
                    variety_penalty += 100000000.0 

                new_cal = sum(r['total_calories'] for r in path) + recipe['total_calories']
                h = float(heuristic(new_cal, target_cal))
                
                new_f = new_g + variety_penalty + h
                
                new_path = path + [recipe]
                heapq.heappush(open_set, (new_f, random.random(), new_path))
        
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
            return {"error": f"Gagal menyusun menu hari ke-{day}."}

    return {
        "menu": final_plan,
        "warnings": warnings
    }