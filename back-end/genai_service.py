import google.generativeai as genai
import json
import re

GOOGLE_API_KEY = "AIzaSyAoxapI81tC0kNGd56_vF4h9Jfc0hNRPw0" 
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')

def generate_recipes_batch(meal_plan_data):
    # Menerima data meal plan, mengumpulkan semua nama masakan, dan meminta resep ringkas sekaligus.
    if "error" in meal_plan_data:
        return {}

    # Kumpulkan semua nama masakan ke dalam list
    dish_list = []
    for day in meal_plan_data.get('menu', []):
        dish_list.append(day['breakfast']['name'])
        dish_list.append(day['lunch']['name'])
        dish_list.append(day['dinner']['name'])

    # Gabungkan jadi string koma
    dishes_str = ", ".join(dish_list)

    # Buat Prompt Khusus JSON
    prompt = f"""
    Saya punya daftar masakan berikut: {dishes_str}.
    
    Tolong buatkan cara memasak SINGKAT (maksimal 2 kalimat padat) untuk SETIAP masakan tersebut.
    
    PENTING:
    1. Output HARUS berupa JSON valid.
    2. Format JSON: {{"Nama Masakan": "Instruksi singkat...", "Nama Masakan 2": "Instruksi..."}}
    3. Jangan gunakan markdown (```json), langsung raw text JSON saja.
    4. Gunakan Bahasa Indonesia.
    """

    try:
        response = model.generate_content(prompt)
        text_response = response.text
        clean_text = re.sub(r'```json\n|```', '', text_response).strip()
        
        # Parsing string JSON ke Dictionary Python
        recipes_dict = json.loads(clean_text)
        return recipes_dict

    except Exception as e:
        print(f"Error GenAI: {e}")
        return {}