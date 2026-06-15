<template>
  <div class="modal-overlay">
    <div class="modal">
      <div class="header">
        <div class="modal-brand">
          <svg width="34" height="34" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="18" cy="14" r="8" stroke="#0d9488" stroke-width="2" fill="#e6fff9"/>
            <path d="M4 40c0-7.7 6.3-14 14-14" stroke="#0d9488" stroke-width="2" stroke-linecap="round"/>
            <path d="M36 22c4 0 7 3 7 7 0 5-7 12-7 12s-7-7-7-12c0-4 3-7 7-7z" stroke="#0d9488" stroke-width="2" fill="#e6fff9"/>
            <circle cx="36" cy="29" r="2.5" fill="#0d9488"/>
          </svg>
          <h2 class="header-title">{{ $t('experts') }}</h2>
        </div>
        <button class="close-btn" @click="$emit('close')">×</button>
      </div>

      <form @submit.prevent="searchExperts" class="form-area">
        <label>
          {{ $t('region') }}:
          <select v-model="region" @change="onRegionChange" required>
            <option disabled value="">{{ $t('select') }}...</option>
            <option v-for="r in regions" :key="r" :value="r">{{ r }}</option>
          </select>
        </label>

        <label>
          {{ $t('district') }}:
          <select v-model="district" required :disabled="!districts.length">
            <option disabled value="">{{ $t('select') }}...</option>
            <option v-for="d in districts" :key="d" :value="d">{{ d }}</option>
          </select>
        </label>

        <button type="submit" :disabled="loading">
          <span v-if="loading" class="loader"></span>
          <span v-else>{{ $t('experts') }}</span>
        </button>
      </form>

      <div class="results" v-if="results.length">
        <h3>{{ $t('available_experts') }}:</h3>
        <ul>
          <li v-for="(expert, i) in results" :key="i">
            <strong>{{ expert.name }}</strong><br />
            <small>{{ expert.contact }} — {{ expert.region }}, {{ expert.district }}</small>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/services/api'
export default {
  emits: ["close", "submit"],
  data() {
    return {
      region: "",
      district: "",
      regions: [],
      districts: [],
      loading: false,
      results: []
    };
  },
  mounted() {
    this.fetchRegions();
  },
  methods: {
    async fetchRegions() {
      this.loading = true;
      try {
        const res = await axios.get("/api/experts/regions/");
        const json = res.data;
        this.regions = json.regions || [];
      } catch (e) {
        console.error("Error fetching regions", e);
      } finally {
        this.loading = false;
      }
    },
    async onRegionChange() {
      this.district = "";
      this.results = [];
      this.districts = [];
      if (!this.region) return;

      this.loading = true;
      try {
        const res = await axios.get(`/api/experts/regions/${encodeURIComponent(this.region)}/districts/`);
        const json = res.data;
        this.districts = json.districts || [];
      } catch (e) {
        console.error("Error fetching districts", e);
      } finally {
        this.loading = false;
      }
    },
    async searchExperts() {
      this.loading = true;
      this.results = [];

      try {
        const res = await axios.get(`/api/experts/search/?region=${this.region}&district=${this.district}`);
        const json = res.data;
        this.results = json.experts || [];
      } catch (e) {
        console.error("Error fetching experts", e);
      } finally {
        this.loading = false;
      }

      this.$emit("submit", {
        region: this.region,
        district: this.district
      });
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.3s ease-out;
  z-index: 1000;
}
.modal {
  background: linear-gradient(to bottom right, #ffffff, #e6fff9);
  border-radius: 20px;
  width: 90%;
  max-width: 500px;
  max-height: 95vh;
  padding: 10px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  animation: scaleIn 0.4s ease;
}
.header {
  padding: 10px;
  margin: 5px auto;
  background-color: var(--chat-header);
  color: var(--primary-teal);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid var(--primary-teal);
  border-radius: 8px;
  width: 92%;
}

.modal-brand {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-title {
  margin: 0;
  font-size: 1.1rem;
  color: var(--primary-teal);
}

.close-btn {
  background: white;
  border: 1px solid var(--primary-teal);
  font-size: 1.2rem;
  color: var(--primary-teal);
  cursor: pointer;
  padding: 0.2rem 0.6rem;
  border-radius: 8px;
  transition: background 0.2s ease;
}

.close-btn:hover {
  background: var(--primary-teal);
  color: white;
}

.form-area {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.form-area label {
  display: flex;
  flex-direction: column;
  font-weight: 600;
}
input,
select {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #ccc;
  margin-top: 5px;
}
button[type="submit"] {
  background: var(--primary-teal);
  color: white;
  padding: 12px;
  border: none;
  border-radius: 12px;
  font-weight: bold;
  cursor: pointer;
}
button[type="submit"]:hover:not(:disabled) {
  background-color: var(--primary-teal-dark);
}

/* Spinner */
.loader {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  vertical-align: middle;
  margin-right: 6px;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.results {
  margin-top: 25px;
}
.results h3 {
  margin-bottom: 10px;
  color: var(--primary-teal);
}
.results ul {
  max-height: 200px;
  overflow-y: auto;
  list-style: none;
  padding: 0;
}
.results li {
  background: white;
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes scaleIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
