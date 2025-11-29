<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

// Input user
const days = ref(1);
const calories = ref(2000);
const budget = ref(100000);
const myPantry = ref([]);
const pantryInput = ref("");

// Data alergi
const availableAllergens = ref([]); 
const selectedAllergies = ref([]); 

// Hasil dan status UI
const menuResult = ref(null);
const loading = ref(false);
const errorMessage = ref("");
const warningMessages = ref([]);
const activeTab = ref("informasi");

// Ambil data alergi saat aplikasi pertama kali dimuat
onMounted(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/allergens");
    availableAllergens.value = response.data;
  } catch (error) {
    console.error("Gagal mengambil data alergi:", error);
  }
});

// Menghitung total belanjaan dari semua menu yang dihasilkan
const shoppingList = computed(() => {
  if (!menuResult.value || !Array.isArray(menuResult.value)) return [];

  const map = {};

  // Iterasi setiap hari dan setiap waktu makan
  menuResult.value.forEach((plan) => {
    ["breakfast", "lunch", "dinner"].forEach((mealKey) => {
      const meal = plan[mealKey];
      if (!meal || !meal.missing_ingredients) return;

      // Agregasi bahan yang perlu dibeli
      meal.missing_ingredients.forEach((item) => {
        if (!map[item.name]) {
          map[item.name] = {
            name: item.name,
            totalAmount: 0,
            unit: item.unit,
            price: item.price_per_unit
          };
        }
        map[item.name].totalAmount += item.amount;
      });
    });
  });

  // Konversi map ke array dan hitung harga total per item
  return Object.values(map).map((item) => {
    const packsToBuy = Math.ceil(item.totalAmount);
    const totalPrice = packsToBuy * item.price;

    return {
      name: item.name,
      amountNeeded: item.totalAmount,
      unit: item.unit,
      packsToBuy: packsToBuy,
      totalPrice: totalPrice
    };
  });
});

// Total biaya keseluruhan belanja
const totalShoppingCost = computed(() => {
  return shoppingList.value.reduce((sum, item) => sum + item.totalPrice, 0);
});

// Menu hari pertama untuk tampilan ringkas "Hari Ini"
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

// Logika Pantry
const addPantry = () => {
  if (pantryInput.value.trim() !== "" && !myPantry.value.includes(pantryInput.value.toLowerCase())) {
    myPantry.value.push(pantryInput.value.toLowerCase());
    pantryInput.value = "";
  }
};
const removePantry = (index) => myPantry.value.splice(index, 1);

// Generate Menu
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
      allergies: selectedAllergies.value,
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
        <h1 class="app-title">MealPlanner AI</h1>
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
              <label>Batas Kalori Harian</label>
              <input type="number" v-model="calories" placeholder="Contoh: 2000" />
            </div>

            <div class="form-group">
              <label>Batas Biaya (Total {{ days }} Hari)</label>
              <input type="number" v-model="budget" placeholder="Contoh: 100000" />
            </div>

            <div class="form-group">
              <label>Alergi</label>
              <div class="allergy-grid">
                <div v-if="availableAllergens.length === 0" class="loading-allergy">
                  Memuat data alergi...
                </div>
                
                <div 
                  v-for="allergen in availableAllergens" 
                  :key="allergen.id" 
                  class="checkbox-item"
                >
                  <input 
                    type="checkbox" 
                    :id="'alg-' + allergen.id" 
                    :value="allergen.id" 
                    v-model="selectedAllergies"
                  />
                  <label :for="'alg-' + allergen.id">{{ allergen.name }}</label>
                </div>
              </div>
            </div>

            <div class="form-group">
              <label>Bahan Masakan yang Sudah Dimiliki</label>
              <div class="input-group">
                <input type="text" v-model="pantryInput" @keyup.enter="addPantry" placeholder="Ketik bahan lalu Enter..." />
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
              {{ loading ? "Sedang Berpikir..." : "Buat Rencana Menu" }}
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
              <p>Belum ada hasil. Silakan isi form dan klik "Buat Rencana Menu".</p>
            </div>

            <div v-else-if="menuResult" class="results-and-shopping">
              <div class="results-tab">
                <div v-for="plan in menuResult" :key="plan.day" class="result-item">
                  <div class="day-header">
                    <h4>Hari ke-{{ plan.day }}</h4>
                    <div class="day-stats">
                      <span class="stat-badge cost">Rp {{ plan.estimated_cost.toLocaleString('id-ID') }}</span>
                      <span class="stat-badge cal">🔥 {{ plan.total_calories }} kkal</span>
                    </div>
                  </div>
                  
                  <div v-for="meal in ['breakfast', 'lunch', 'dinner']" :key="meal" class="meal-detail">
                    <strong>{{ meal === 'breakfast' ? 'Sarapan' : meal === 'lunch' ? 'Siang' : 'Malam' }}:</strong> 
                    {{ plan[meal].name }}
                    
                    <small v-if="plan[meal].missing_ingredients.length" style="display:block; margin-top:2px;">
                      <span style="color:#d32f2f;">Beli: </span> 
                      <span v-for="(ing, i) in plan[meal].missing_ingredients" :key="i">
                        {{ ing.name }} ({{ ing.amount.toFixed(2) }} {{ ing.unit }}){{ i < plan[meal].missing_ingredients.length - 1 ? ', ' : '' }}
                      </span>
                    </small>
                  </div>
                </div>
              </div>

              <div class="shopping-box card" style="margin-top: 20px; border: 2px solid #2d5016;">
                <h4 style="margin-top: 0; color: #2d5016; text-align:center;">🛒 DAFTAR BELANJA TOTAL</h4>
                <p style="text-align:center; font-size:13px; color:#666; margin-bottom:15px;">
                  Harga kemasan yang umum tersedia di pasaran
                </p>

                <ul v-if="shoppingList.length" style="list-style: none; padding: 0; margin: 0">
                  <li v-for="(it, idx) in shoppingList" :key="idx" class="shopping-item">
                    <div style="display:flex; flex-direction:column;">
                      <span style="font-weight:bold; font-size:14px;">{{ it.name }}</span>
                      <span style="font-size:12px; color:#555;">
                        Butuh: {{ it.amountNeeded.toFixed(2) }} {{ it.unit }} 
                        → <strong>Beli {{ it.packsToBuy }} Pack</strong>
                      </span>
                    </div>
                    <span style="font-weight: bold; color: #d32f2f; font-size:14px;">
                      Rp {{ it.totalPrice.toLocaleString('id-ID') }}
                    </span>
                  </li>
                </ul>
                <p v-else style="color:#999; font-style:italic; text-align:center;">Semua bahan tersedia di pantry!</p>

                <div v-if="shoppingList.length" style="margin-top:20px; padding-top:10px; border-top:2px solid #eee; display:flex; justify-content:space-between; align-items:center;">
                  <strong style="font-size:16px;">EST. TOTAL BIAYA:</strong>
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
          <p v-if="!menuResult" class="no-menu">Menu belum dibuat</p>
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  letter-spacing: 1px;
}

.header-decoration {
  font-size: 30px;
}

/* MAIN CONTAINER */
.main-container {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 30px 20px;
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 30px;
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
}

/* TABS */
.tabs {
  display: flex;
  border-bottom: 2px solid #e0e0e0;
  margin-bottom: 25px;
}

.tab-btn {
  flex: 1;
  padding: 12px;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 600;
  color: #666;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.tab-btn:hover, .tab-btn.active {
  color: #2d5016;
  background: #f9f9f9;
}

.tab-btn.active {
  border-bottom-color: #2d5016;
}

.tab-content {
  animation: fadeIn 0.3s ease;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

.tab-desc {
  color: #777;
  font-size: 14px;
  margin-bottom: 20px;
  font-style: italic;
}

/* FORM STYLES */
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
  padding: 10px;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.form-group input:focus {
  outline: none;
  border-color: #2d5016;
  box-shadow: 0 0 0 3px rgba(45, 80, 22, 0.1);
}

/* --- STYLE UNTUK CHECKBOX ALERGI --- */
.allergy-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 10px;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  max-height: 200px;
  overflow-y: auto;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  cursor: pointer;
  background: white;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #eee;
  transition: all 0.2s;
}

.checkbox-item:hover {
  border-color: #a8d5a8;
  background: #f0fff4;
}

.checkbox-item input {
  width: 16px;
  height: 16px;
  accent-color: #2d5016;
  cursor: pointer;
}

.checkbox-item label {
  margin: 0 !important;
  font-weight: normal !important;
  cursor: pointer;
  color: #333 !important;
}

.loading-allergy {
  grid-column: 1 / -1;
  text-align: center;
  color: #999;
  font-style: italic;
  font-size: 13px;
}

/* INPUT GROUP & TAGS */
.input-group {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.btn-add {
  background: #a8d5a8;
  color: white;
  border: none;
  padding: 0 16px;
  border-radius: 8px;
  font-size: 20px;
  cursor: pointer;
  font-weight: bold;
}
.btn-add:hover { background: #90c890; }

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: #e8f5e9;
  border: 1px solid #a8d5a8;
  color: #2d5016;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.remove-btn {
  cursor: pointer;
  font-weight: bold;
  opacity: 0.6;
}
.remove-btn:hover { opacity: 1; }

/* BUTTON GENERATE */
.btn-generate {
  width: 100%;
  padding: 14px;
  background: #2d5016;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
  transition: background 0.3s;
}
.btn-generate:hover:not(:disabled) { background: #1f3810; }
.btn-generate:disabled { background: #ccc; cursor: not-allowed; }

/* RESULTS STYLES */
.result-item {
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
  border-left: 4px solid #2d5016;
  margin-bottom: 15px;
}

.day-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 8px;
}

.day-header h4 { margin: 0; color: #2d5016; }

.stat-badge {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: bold;
  margin-left: 5px;
}

.stat-badge.cost { background: #fff3cd; color: #856404; }
.stat-badge.cal { background: #d4edda; color: #155724; }

.meal-detail {
  font-size: 14px;
  margin: 8px 0;
  color: #444;
  line-height: 1.4;
}

.shopping-item {
  padding: 10px 0;
  border-bottom: 1px dashed #ccc;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.warning-box {
  background: #fff3cd;
  color: #856404;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 15px;
  font-size: 14px;
}
.error-msg {
  background: #ffebee;
  color: #c62828;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 15px;
}

/* RIGHT PANEL */
.menu-today {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 25px;
}
.menu-today h2 { margin-top: 0; font-size: 18px; color: #333; }
.no-menu { text-align: center; color: #999; margin: 30px 0; font-style: italic; }

.menu-item {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  background: #2d5016;
  color: white;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: transform 0.2s;
}
.menu-item:hover { transform: translateX(5px); }

.menu-item-left h3 { margin: 0 0 5px 0; font-size: 15px; }
.menu-item-left p { margin: 0; font-size: 13px; opacity: 0.9; }

.menu-item-right {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(255,255,255,0.2);
  padding: 5px 10px;
  border-radius: 6px;
  min-width: 70px;
}
.day-num { font-size: 10px; text-transform: uppercase; }
.date { font-size: 18px; font-weight: bold; }
.time-info { font-size: 10px; }

/* RESPONSIVE */
@media (max-width: 900px) {
  .main-container { grid-template-columns: 1fr; }
}
</style>