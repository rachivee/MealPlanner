<script setup>
import { ref, computed } from "vue";
import axios from "axios";

const days = ref(1);
const calories = ref(2000);
const budget = ref(100000);

const myPantry = ref([]);
const pantryInput = ref(""); 
const myAllergies = ref([]);
const allergyInput = ref("");

const menuResult = ref(null);
const loading = ref(false);
const errorMessage = ref("");
const warningMessages = ref([]); 
const activeTab = ref("informasi");

// --- LOGIKA BARU: REALISTIC SHOPPING LIST ---
const shoppingList = computed(() => {
  if (!menuResult.value || !Array.isArray(menuResult.value)) return [];
  
  const map = {};

  // 1. Kumpulkan semua kebutuhan bahan
  menuResult.value.forEach((plan) => {
    ["breakfast", "lunch", "dinner"].forEach((mealKey) => {
      const meal = plan[mealKey];
      if (!meal || !meal.missing_ingredients) return;
      
      meal.missing_ingredients.forEach((item) => {
        // item sekarang adalah object {name, amount, unit, price_per_unit}
        if (!map[item.name]) {
          map[item.name] = {
            name: item.name,
            totalAmount: 0,
            unit: item.unit,
            price: item.price_per_unit
          };
        }
        // Akumulasi jumlah yang dibutuhkan
        map[item.name].totalAmount += item.amount;
      });
    });
  });

  // 2. Hitung Berapa Pack yang harus dibeli
  return Object.values(map).map((item) => {
    // Pembulatan ke atas (beli kemasan utuh)
    const packsToBuy = Math.ceil(item.totalAmount);
    const totalPrice = packsToBuy * item.price;

    return {
      name: item.name,
      amountNeeded: item.totalAmount, // misal 0.4
      unit: item.unit,
      packsToBuy: packsToBuy,         // misal 1
      totalPrice: totalPrice          // Harga 1 pack
    };
  });
});

// Hitung total belanja keseluruhan
const totalShoppingCost = computed(() => {
  return shoppingList.value.reduce((sum, item) => sum + item.totalPrice, 0);
});

const todaysMenu = computed(() => {
  if (!menuResult.value || !menuResult.value[0]) return [];
  const day1 = menuResult.value[0];
  const list = [
    { name: day1.breakfast?.name, time: 'Sarapan', timing: 'Pukul 07:00' },
    { name: day1.lunch?.name, time: 'Makan Siang', timing: 'Pukul 12:00' },
    { name: day1.dinner?.name, time: 'Makan Malam', timing: 'Pukul 19:00' },
  ];
  return list.filter(item => item.name);
});

const addPantry = () => {
  if (pantryInput.value.trim() !== "" && !myPantry.value.includes(pantryInput.value.toLowerCase())) {
    myPantry.value.push(pantryInput.value.toLowerCase());
    pantryInput.value = "";
  }
};
const removePantry = (index) => myPantry.value.splice(index, 1);

const addAllergy = () => {
  if (allergyInput.value.trim() !== "" && !myAllergies.value.includes(allergyInput.value.toLowerCase())) {
    myAllergies.value.push(allergyInput.value.toLowerCase());
    allergyInput.value = "";
  }
};
const removeAllergy = (index) => myAllergies.value.splice(index, 1);

const generateMenu = async () => {
  loading.value = true;
  menuResult.value = null;
  errorMessage.value = "";
  warningMessages.value = [];

  try {
    const response = await axios.post("http://127.0.0.1:5000/generate-menu", {
      days: days.value,
      calories: calories.value,
      budget: budget.value,
      pantry: myPantry.value,
      allergies: myAllergies.value,
    });

    if (response.data.error) {
      errorMessage.value = response.data.error;
    } else {
      menuResult.value = response.data.menu;
      warningMessages.value = response.data.warnings || [];
      activeTab.value = 'hasil';
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
  <div class="app-wrapper">
    <header class="app-header">
      <div class="header-content">
        <h1 class="app-title">MealPlanner</h1>
        <div class="header-decoration">🍽️</div>
      </div>
    </header>

    <div class="main-container">
      <div class="left-panel">
        <div class="card input-box">
          <h2>MEAL PLANNER</h2>

          <div class="tabs">
            <button class="tab-btn" :class="{ active: activeTab === 'informasi' }" @click="activeTab = 'informasi'">Informasi</button>
            <button class="tab-btn" :class="{ active: activeTab === 'hasil' }" @click="activeTab = 'hasil'">Hasil & List Belanja</button>
          </div>

          <div v-if="activeTab === 'informasi'" class="tab-content">
            <p class="tab-desc">Isi form dibawah sesuaikan dengan preferensi anda</p>

            <div class="form-group">
              <label>Batas Kalori</label>
              <input type="number" v-model="calories" placeholder="Contoh: 2000" />
            </div>

            <div class="form-group">
              <label>Batas Biaya (Total {{ days }} Hari)</label>
              <input type="number" v-model="budget" placeholder="Contoh: 100000" />
            </div>

            <div class="form-group">
              <label>Alergi</label>
              <div class="input-group">
                <input type="text" v-model="allergyInput" @keyup.enter="addAllergy" placeholder="Ketik alergi..." />
                <button class="btn-add" @click="addAllergy">+</button>
              </div>
              <div class="tags">
                <span v-for="(item, index) in myAllergies" :key="index" class="tag allergy">
                  {{ item }} <span class="remove-btn" @click="removeAllergy(index)">×</span>
                </span>
              </div>
            </div>

            <div class="form-group">
              <label>Bahan Masakan Tersedia</label>
              <div class="input-group">
                <input type="text" v-model="pantryInput" @keyup.enter="addPantry" placeholder="Ketik bahan..." />
                <button class="btn-add" @click="addPantry">+</button>
              </div>
              <div class="tags">
                <span v-for="(item, index) in myPantry" :key="index" class="tag">
                  {{ item }} <span class="remove-btn" @click="removePantry(index)">×</span>
                </span>
              </div>
            </div>

            <div class="form-group">
              <label>Jumlah Hari</label>
              <input type="number" v-model="days" min="1" max="7" />
            </div>

            <button class="btn-generate" @click="generateMenu" :disabled="loading">
              {{ loading ? "Sedang Berpikir..." : "Buat Rencana" }}
            </button>
          </div>

          <div v-if="activeTab === 'hasil'" class="tab-content">
            <div v-if="errorMessage" class="error-msg">⚠️ {{ errorMessage }}</div>

            <div v-if="warningMessages.length > 0" class="warning-box">
              <h4>⚠️ Perhatian</h4>
              <ul>
                <li v-for="(msg, idx) in warningMessages" :key="idx">{{ msg }}</li>
              </ul>
            </div>

            <div v-if="!menuResult && !errorMessage" class="empty-state">
              <p>Belum ada hasil. Klik "Buat Rencana".</p>
            </div>

            <div v-else-if="menuResult" class="results-and-shopping">
              <div class="results-tab">
                <div v-for="plan in menuResult" :key="plan.day" class="result-item">
                  <div class="day-header">
                    <h4>Hari ke-{{ plan.day }}</h4>
                    <div class="day-stats">
                      <span class="stat-badge cost">Est. Makan: Rp {{ plan.estimated_cost.toLocaleString('id-ID') }}</span>
                      <span class="stat-badge cal">🔥 {{ plan.total_calories }} kkal</span>
                    </div>
                  </div>
                  
                  <div v-for="meal in ['breakfast', 'lunch', 'dinner']" :key="meal" class="meal-detail">
                    <strong>{{ meal === 'breakfast' ? 'Sarapan' : meal === 'lunch' ? 'Siang' : 'Malam' }}:</strong> 
                    {{ plan[meal].name }}
                    
                    <small v-if="plan[meal].missing_ingredients.length" style="display:block; margin-top:2px;">
                      <span style="color:#d32f2f;">Beli: </span> 
                      <span v-for="(ing, i) in plan[meal].missing_ingredients" :key="i">
                        {{ ing.name }} ({{ ing.amount }} {{ ing.unit }}){{ i < plan[meal].missing_ingredients.length - 1 ? ', ' : '' }}
                      </span>
                    </small>
                  </div>
                </div>
              </div>

              <div class="shopping-box card" style="margin-top: 16px; border: 2px solid #2d5016;">
                <h4 style="margin-top: 0; color: #2d5016; text-align:center;">🛒 DAFTAR BELANJA TOTAL</h4>
                <p style="text-align:center; font-size:13px; color:#666; margin-bottom:15px;">
                  Estimasi belanja (Beli Kemasan Utuh)
                </p>

                <ul v-if="shoppingList.length" style="list-style: none; padding: 0; margin: 0">
                  <li v-for="(it, idx) in shoppingList" :key="idx" style="padding: 10px 0; border-bottom: 1px dashed #ccc; display: flex; justify-content: space-between; align-items: center;">
                    
                    <div style="display:flex; flex-direction:column;">
                      <span style="font-weight:bold; font-size:14px;">{{ it.name }}</span>
                      <span style="font-size:12px; color:#555;">
                        Butuh: {{ it.amountNeeded.toFixed(1) }} {{ it.unit }} 
                        → <strong>Beli {{ it.packsToBuy }} Pack</strong>
                      </span>
                    </div>

                    <span style="font-weight: bold; color: #d32f2f; font-size:14px;">
                      Rp {{ it.totalPrice.toLocaleString('id-ID') }}
                    </span>
                  </li>
                </ul>
                <p v-else style="color:#999; font-style:italic; text-align:center;">Semua bahan tersedia di kulkas.</p>

                <div v-if="shoppingList.length" style="margin-top:20px; padding-top:10px; border-top:2px solid #eee; display:flex; justify-content:space-between; align-items:center;">
                  <strong style="font-size:16px;">TOTAL HARUS DIBAYAR:</strong>
                  <strong style="font-size:18px; color:#2d5016;">Rp {{ totalShoppingCost.toLocaleString('id-ID') }}</strong>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="right-panel">
        <div class="menu-today">
          <h2>MAKANANMU HARI INI</h2>
          <p v-if="!menuResult" class="no-menu">Buat rencana terlebih dahulu</p>
          <div v-else class="menu-list">
            <div v-for="meal in todaysMenu" :key="meal.time" class="menu-item">
              <div class="menu-item-left">
                <h3>{{ meal.name }}</h3>
                <p>{{ meal.time }}</p>
              </div>
              <div class="menu-item-right">
                <span class="day-num">Hari</span>
                <span class="date">1</span>
                <span class="time-info">{{ meal.timing }}</span>
              </div>
            </div>
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

.header-decoration {
  font-size: 40px;
}

/* MAIN CONTAINER */
.main-container {
  flex: 1;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  padding: 30px 20px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

/* PANELS */
.left-panel {
  flex: 1;
}

.right-panel {
  flex: 1;
}

/* CARD STYLES */
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 30px;
}

.input-box h2 {
  margin: 0 0 20px 0;
  font-size: 20px;
  font-weight: bold;
  color: #1a1a1a;
  letter-spacing: 1px;
}

/* TAB NAVIGATION */
.tabs {
  display: flex;
  gap: 0;
  border-bottom: 2px solid #e0e0e0;
  margin-bottom: 25px;
}

.tab-btn {
  flex: 1;
  padding: 12px 16px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #666;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  text-align: center;
  text-transform: capitalize;
}

.tab-btn:hover {
  color: #2d5016;
  background: #f5f5f5;
}

.tab-btn.active {
  color: #2d5016;
  border-bottom-color: #2d5016;
}

/* TAB CONTENT */
.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tab-desc {
  color: #777;
  font-size: 14px;
  margin-bottom: 20px;
  font-style: italic;
}

/* FORM GROUPS */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 14px;
  color: #2d5016;
}

.form-group input[type="number"],
.form-group input[type="text"] {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #2d5016;
  box-shadow: 0 0 0 3px rgba(45, 80, 22, 0.1);
}

/* INPUT GROUP */
.input-group {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.input-group input {
  flex: 1;
}

.btn-add {
  background: #a8d5a8;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.3s ease;
  font-weight: bold;
}

.btn-add:hover {
  background: #90c890;
}

/* TAGS */
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
  min-height: 20px;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #e8f5e9;
  border: 1px solid #a8d5a8;
  color: #2d5016;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.tag.allergy {
  background: #ffebee;
  border-color: #ef5350;
  color: #c62828;
}

.remove-btn {
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.remove-btn:hover {
  opacity: 1;
}

/* BUTTON GENERATE */
.btn-generate {
  width: 100%;
  padding: 14px 20px;
  background: #2d5016;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
  margin-top: 20px;
  letter-spacing: 0.5px;
}

.btn-generate:hover:not(:disabled) {
  background: #1f3810;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(45, 80, 22, 0.25);
}

.btn-generate:disabled {
  background: #bdbdbd;
  cursor: not-allowed;
}

/* FEEDBACK MESSAGES (Error & Empty State) */
.error-msg {
  background: #ffebee;
  color: #b71c1c;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #ef5350;
  margin-bottom: 20px;
  font-size: 14px;
}

.empty-state {
  padding: 30px 20px;
  text-align: center;
  color: #999;
}

.empty-state p {
  margin: 0;
  font-style: italic;
}

/* STYLE BARU: WARNING BOX */
.warning-box {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}
.warning-box h4 { margin: 0 0 8px 0; font-size: 14px; }
.warning-box ul { margin: 0; padding-left: 20px; font-size: 13px; }

/* RESULTS TAB */
.results-tab {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.result-item {
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
  border-left: 4px solid #2d5016;
}

.result-item h4 {
  margin: 0 0 10px 0;
  color: #2d5016;
  font-size: 14px;
}

.meal-detail {
  font-size: 13px;
  margin: 5px 0;
  color: #555;
}

.day-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 8px;
}

.day-header h4 {
  margin: 0; /* Hilangkan margin bawaan h4 agar sejajar */
}

.day-stats {
  display: flex;
  gap: 8px;
}

.stat-badge {
  font-size: 12px;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 6px;
}

.stat-badge.cost {
  background-color: #fff3cd; /* Kuning muda */
  color: #856404;
  border: 1px solid #ffeeba;
}

.stat-badge.cal {
  background-color: #d4edda; /* Hijau muda */
  color: #155724;
  border: 1px solid #c3e6cb;
}

/* BAHAN LIST */
.bahan-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.bahan-item {
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
  border-left: 4px solid #ff6b6b;
}

.bahan-item h4 {
  margin: 0 0 10px 0;
  color: #ff6b6b;
  font-size: 14px;
}

.bahan-item ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.bahan-item li {
  font-size: 13px;
  color: #555;
  margin: 5px 0;
  padding-left: 10px;
}

/* RIGHT PANEL - MENU TODAY */
.menu-today {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 30px;
}

.menu-today h2 {
  margin: 0 0 15px 0;
  font-size: 18px;
  font-weight: bold;
  color: #1a1a1a;
  letter-spacing: 1px;
}

.no-menu {
  text-align: center;
  color: #999;
  padding: 40px 20px;
  font-style: italic;
}

.menu-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px;
  background: #2d5016;
  color: white;
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.menu-item:hover {
  transform: translateX(5px);
  box-shadow: 0 6px 20px rgba(45, 80, 22, 0.3);
}

.menu-item-left h3 {
  margin: 0 0 5px 0;
  font-size: 15px;
  font-weight: 600;
}

.menu-item-left p {
  margin: 0;
  font-size: 13px;
  opacity: 0.9;
}

.menu-item-right {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 13px;
  text-align: center;
}

.day-num {
  font-size: 11px;
  opacity: 0.8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.date {
  font-size: 18px;
  font-weight: bold;
}

.time-info {
  font-size: 11px;
  opacity: 0.8;
}

/* RESPONSIVE */
@media (max-width: 1024px) {
  .main-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .app-header {
    padding: 15px 0;
  }

  .app-title {
    font-size: 22px;
  }

  .header-decoration {
    font-size: 30px;
  }

  .main-container {
    padding: 20px 15px;
  }

  .card {
    padding: 20px;
  }

  .tabs {
    gap: 5px;
  }

  .tab-btn {
    font-size: 12px;
    padding: 10px 8px;
  }

  .menu-item {
    flex-direction: column;
    gap: 10px;
  }

  .menu-item-right {
    width: 100%;
    flex-direction: row;
  }
}
</style>