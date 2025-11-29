<script setup>
import { ref, computed } from "vue";
import axios from "axios";

// --- DATA NEGARA (STATE) ---
const days = ref(1);
const calories = ref(2000);
const budget = ref(100000); // DEFAULT BUDGET (Rp 100.000)

const myPantry = ref([]);
const pantryInput = ref(""); 
const myAllergies = ref([]);
const allergyInput = ref("");

const menuResult = ref(null);
const loading = ref(false);
const errorMessage = ref("");
const activeTab = ref("informasi"); // Tab aktif: informasi, hasil

// computed shopping list: gabungkan semua missing_ingredients dari setiap meal
const shoppingList = computed(() => {
  if (!menuResult.value || !Array.isArray(menuResult.value)) return [];
  const counts = {};
  menuResult.value.forEach((plan) => {
    ["breakfast", "lunch", "dinner"].forEach((mealKey) => {
      const meal = plan[mealKey];
      if (!meal || !meal.missing_ingredients) return;
      meal.missing_ingredients.forEach((it) => {
        const name = String(it).trim();
        if (!name) return;
        counts[name] = (counts[name] || 0) + 1;
      });
    });
  });
  return Object.keys(counts).map((k) => ({ name: k, qty: counts[k] }));
});

// --- FUNGSI UTILS ---
const addPantry = () => {
  if (pantryInput.value.trim() !== "" && !myPantry.value.includes(pantryInput.value.toLowerCase())) {
    myPantry.value.push(pantryInput.value.toLowerCase());
    pantryInput.value = "";
  }
};
const removePantry = (index) => myPantry.value.splice(index, 1);

const addAllergy = () => {
  if (
    allergyInput.value.trim() !== "" &&
    !myAllergies.value.includes(allergyInput.value.toLowerCase())
  ) {
    myAllergies.value.push(allergyInput.value.toLowerCase());
    allergyInput.value = "";
  }
};
const removeAllergy = (index) => myAllergies.value.splice(index, 1);

// --- REQUEST KE PYTHON ---
const generateMenu = async () => {
  loading.value = true;
  menuResult.value = null;
  errorMessage.value = "";

  try {
    const response = await axios.post("http://127.0.0.1:5000/generate-menu", {
      days: days.value,
      calories: calories.value,
      budget: budget.value, // KIRIM BUDGET KE PYTHON
      pantry: myPantry.value,
      allergies: myAllergies.value,
    });

    if (response.data.error) {
      errorMessage.value = response.data.error;
    } else {
      menuResult.value = response.data;
    }
  } catch (error) {
    console.error(error);
    errorMessage.value = "Gagal konek ke Server.";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="container">
    <h1>🍱 Smart Meal Planner AI</h1>
    <p>Fitur Baru: <b>Budget Limiter</b> (Anti Boncos)</p>

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

      <div class="form-group" style="margin-bottom: 20px;">
        <label>💰 Batas Budget Total (Rupiah):</label>
        <input type="number" v-model="budget" placeholder="Contoh: 50000" style="background: #fff8e1; border-color: #ffc107;">
        <small style="color: #666;">AI tidak akan memberi menu yang total belanjanya melebihi ini.</small>
      </div>

      <label>Bahan di Kulkas:</label>
      <div class="input-group">
        <input type="text" v-model="pantryInput" @keyup.enter="addPantry" placeholder="Ketik bahan lalu Enter...">
        <button class="btn-add" @click="addPantry">+</button>
      </div>
      <div class="tags">
        <span v-for="(item, index) in myPantry" :key="index" class="tag active">
          {{ item }} <span class="remove-btn" @click="removePantry(index)">×</span>
        </span>
      </div>

      <label style="margin-top: 20px;">Alergi:</label>
      <div class="input-group">
        <input type="text" v-model="allergyInput" @keyup.enter="addAllergy" placeholder="Ketik alergi lalu Enter...">
        <button class="btn-add" @click="addAllergy">+</button>
      </div>
      <div class="tags">
        <span v-for="(item, index) in myAllergies" :key="index" class="tag allergy active">
          {{ item }} <span class="remove-btn" @click="removeAllergy(index)">×</span>
        </span>
      </div>

      <button class="btn-generate" @click="generateMenu" :disabled="loading">
        {{ loading ? 'Sedang Menghitung...' : 'GENERATE MENU' }}
      </button>
    </div>

    <div v-if="errorMessage" class="error-msg">⚠️ {{ errorMessage }}</div>

    <div v-if="menuResult" class="results">
      <div class="budget-summary">
        Total Estimasi Belanja: <b>Rp {{ menuResult.reduce((sum, item) => sum + item.estimated_cost, 0) }}</b>
        (Batas: Rp {{ budget }})
      </div>

      <div v-for="plan in menuResult" :key="plan.day" class="menu-card">
        <div class="card-head">
          <h3>Hari ke-{{ plan.day }}</h3>
          <span class="badge cost">Belanja: Rp {{ plan.estimated_cost }}</span>
          <span class="badge cal">Kalori: {{ plan.total_calories }}</span>
        </div>
        
        <div class="meal-row">
          <div v-for="mealType in ['breakfast', 'lunch', 'dinner']" :key="mealType" class="meal">
            <span class="label">{{ mealType }}</span>
            <strong>{{ plan[mealType].name }}</strong>
            <small v-if="plan[mealType].missing_ingredients.length" class="missing">
              Beli: {{ plan[mealType].missing_ingredients.join(', ') }}
            </small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* GLOBAL STYLES */
* {
  box-sizing: border-box;
}

.app-wrapper {
  background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* HEADER */
.app-header {
  background: linear-gradient(90deg, #2d5016 0%, #3d6b1f 100%);
  color: white;
  padding: 20px 0;
  box-shadow: 0 4px 12px rgba(45, 80, 22, 0.15);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title {
  font-size: 28px;
  font-weight: bold;
  margin: 0;
  letter-spacing: 1px;
}

.budget-summary {
  background: #e8f5e9; color: #2e7d32; padding: 15px; border-radius: 8px; 
  text-align: center; margin-bottom: 20px; border: 1px solid #a5d6a7;
}
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
