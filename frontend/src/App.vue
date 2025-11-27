<script setup>
import { ref } from 'vue';
import axios from 'axios';

// --- DATA NEGARA (STATE) ---
const days = ref(1);
const calories = ref(2000);

// Kita tidak butuh lagi "availableIngredients" karena user input sendiri
const myPantry = ref([]);     // Daftar bahan yang user punya
const pantryInput = ref("");  // Tempat user mengetik sementara

const myAllergies = ref([]);    // Daftar alergi user
const allergyInput = ref("");   // Tempat user mengetik alergi

const menuResult = ref(null);
const loading = ref(false);
const errorMessage = ref("");

// --- FUNGSI TAMBAH/HAPUS BAHAN ---
const addPantry = () => {
  // Cek agar tidak kosong dan tidak duplikat
  if (pantryInput.value.trim() !== "" && !myPantry.value.includes(pantryInput.value.toLowerCase())) {
    myPantry.value.push(pantryInput.value.toLowerCase()); // Simpan huruf kecil biar cocok sama DB
    pantryInput.value = ""; // Bersihkan kolom input
  }
};

const removePantry = (index) => {
  myPantry.value.splice(index, 1);
};

// --- FUNGSI TAMBAH/HAPUS ALERGI ---
const addAllergy = () => {
  if (allergyInput.value.trim() !== "" && !myAllergies.value.includes(allergyInput.value.toLowerCase())) {
    myAllergies.value.push(allergyInput.value.toLowerCase());
    allergyInput.value = "";
  }
};

const removeAllergy = (index) => {
  myAllergies.value.splice(index, 1);
};

// --- FUNGSI MINTA MENU KE PYTHON ---
const generateMenu = async () => {
  loading.value = true;
  menuResult.value = null;
  errorMessage.value = "";

  try {
    const response = await axios.post('http://127.0.0.1:5000/generate-menu', {
      days: days.value,
      calories: calories.value,
      pantry: myPantry.value,
      allergies: myAllergies.value
    });

    if (response.data.error) {
      errorMessage.value = response.data.error;
    } else {
      menuResult.value = response.data;
    }
    
  } catch (error) {
    console.error(error);
    errorMessage.value = "Gagal konek ke Server. Pastikan terminal Backend nyala!";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="container">
    <h1>🍱 Smart Meal Planner AI</h1>
    <p>Ketik bahan yang kamu punya, lalu tekan Enter.</p>

    <div class="card input-box">
      <div class="row">
        <div class="col">
          <label>Jumlah Hari:</label>
          <input type="number" v-model="days" min="1" max="7">
        </div>
        <div class="col">
          <label>Target Kalori:</label>
          <input type="number" v-model="calories">
        </div>
      </div>

      <label>Bahan di Kulkas:</label>
      <div class="input-group">
        <input type="text" v-model="pantryInput" @keyup.enter="addPantry" placeholder="Ketik bahan (contoh: Telur)...">
        <button class="btn-add" @click="addPantry">+</button>
      </div>
      
      <div class="tags">
        <span v-for="(item, index) in myPantry" :key="index" class="tag active">
          {{ item }}
          <span class="remove-btn" @click="removePantry(index)">×</span>
        </span>
        <span v-if="myPantry.length === 0" class="empty-text">Belum ada bahan.</span>
      </div>

      <label style="margin-top: 20px;">Alergi:</label>
      <div class="input-group">
        <input type="text" v-model="allergyInput" @keyup.enter="addAllergy" placeholder="Ketik alergi (contoh: Kacang)...">
        <button class="btn-add" @click="addAllergy">+</button>
      </div>

      <div class="tags">
        <span v-for="(item, index) in myAllergies" :key="index" class="tag allergy active">
          {{ item }}
          <span class="remove-btn" @click="removeAllergy(index)">×</span>
        </span>
      </div>

      <button class="btn-generate" @click="generateMenu" :disabled="loading">
        {{ loading ? 'Sedang Berpikir...' : 'GENERATE MENU' }}
      </button>
    </div>

    <div v-if="errorMessage" class="error-msg">
      ⚠️ {{ errorMessage }}
    </div>

    <div v-if="menuResult" class="results">
      <div v-for="plan in menuResult" :key="plan.day" class="menu-card">
        <div class="card-head">
          <h3>Hari ke-{{ plan.day }}</h3>
          <span class="badge cost">Belanja: Rp {{ plan.estimated_cost }}</span>
          <span class="badge cal">Kalori: {{ plan.total_calories }}</span>
        </div>
        
        <div class="meal-row">
          <div class="meal" v-if="plan.breakfast">
            <span class="label">Pagi</span>
            <strong>{{ plan.breakfast.name }}</strong>
            <small v-if="plan.breakfast.missing_ingredients.length" class="missing">
              Beli: {{ plan.breakfast.missing_ingredients.join(', ') }}
            </small>
          </div>
          
          <div class="meal" v-if="plan.lunch">
            <span class="label">Siang</span>
            <strong>{{ plan.lunch.name }}</strong>
            <small v-if="plan.lunch.missing_ingredients.length" class="missing">
              Beli: {{ plan.lunch.missing_ingredients.join(', ') }}
            </small>
          </div>
          
          <div class="meal" v-if="plan.dinner">
            <span class="label">Malam</span>
            <strong>{{ plan.dinner.name }}</strong>
            <small v-if="plan.dinner.missing_ingredients.length" class="missing">
              Beli: {{ plan.dinner.missing_ingredients.join(', ') }}
            </small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
/* CSS UPDATE */
body { font-family: sans-serif; background: #f4f4f9; padding: 20px; color: #333; }
.container { max-width: 700px; margin: 0 auto; }
h1 { text-align: center; margin-bottom: 5px; }
p { text-align: center; color: #666; margin-bottom: 25px; }

.card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; }
.row { display: flex; gap: 15px; margin-bottom: 20px; }
.col { flex: 1; }
input[type="number"], input[type="text"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; box-sizing: border-box; }
label { display: block; font-weight: bold; margin-bottom: 8px; font-size: 0.9em; }

/* Styling Input Manual */
.input-group { display: flex; gap: 10px; margin-bottom: 10px; }
.btn-add { background: #4caf50; color: white; border: none; padding: 0 20px; border-radius: 8px; font-size: 1.5rem; cursor: pointer; }

.tags { display: flex; flex-wrap: wrap; gap: 10px; min-height: 30px; align-items: center; }
.tag { padding: 6px 12px; background: #e3f2fd; border: 1px solid #2196f3; color: #0d47a1; border-radius: 20px; font-size: 0.9em; display: inline-flex; align-items: center; gap: 8px; font-weight: bold; }
.tag.allergy { background: #ffebee; border-color: #ef5350; color: #c62828; }
.remove-btn { cursor: pointer; font-size: 1.2em; line-height: 0.8; opacity: 0.6; }
.remove-btn:hover { opacity: 1; }
.empty-text { font-style: italic; color: #999; font-size: 0.9em; }

.btn-generate { width: 100%; padding: 14px; background: #2196f3; color: white; border: none; border-radius: 8px; font-size: 1.1rem; cursor: pointer; margin-top: 25px; font-weight: bold; transition: 0.2s; }
.btn-generate:disabled { background: #b0bec5; }

/* ... CSS Kartu Menu sama seperti sebelumnya ... */
.error-msg { background: #ffcdd2; color: #b71c1c; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 20px; border: 1px solid #ef9a9a; }
.menu-card { background: white; border-radius: 12px; overflow: hidden; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.card-head { background: #263238; color: white; padding: 12px 20px; display: flex; align-items: center; gap: 10px; }
.card-head h3 { margin: 0; flex: 1; font-size: 1.1em; }
.badge { font-size: 0.8em; padding: 4px 8px; border-radius: 6px; font-weight: bold; }
.badge.cost { background: #ffd600; color: #333; }
.badge.cal { background: #66bb6a; color: white; }
.meal-row { padding: 20px; display: grid; gap: 15px; }
.meal { border-bottom: 1px solid #f0f0f0; padding-bottom: 15px; }
.meal:last-child { border-bottom: none; padding-bottom: 0; }
.label { display: inline-block; width: 60px; font-size: 0.75em; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px; }
.missing { display: block; color: #e53935; font-size: 0.85em; margin-left: 64px; margin-top: 4px; font-style: italic; }
</style>