<template>
  <div class="modal-overlay">
    <transition name="modal-grow" mode="out-in">
      <div class="modal">
        <h2>{{ $t('followup_support') }}</h2>

        <p class="guide" v-if="!success">{{ $t('followup_instruction') }}</p>

        <!-- Form -->
        <div class="intro-form" v-if="!success">
          <label>{{ $t('contact_info') }}</label>
          <input v-model="form.contact_info" type="text" :placeholder="$t('enter_contact')" />

          <label>{{ $t('location') }}</label>
          <input v-model="form.location" type="text" :placeholder="$t('enter_location')" />

          <label>{{ $t('description') }}</label>
          <textarea v-model="form.description" :placeholder="$t('enter_description')"></textarea>

          <button :disabled="!form.contact_info || !form.location || loading" @click="submitForm">
            <span v-if="loading" class="spinner"></span>
            {{ $t('submit') }}
          </button>

          <p v-if="errorMessage" disabled class="error-msg">{{ errorMessage }}</p>
        </div>

        <!-- Success message -->
        <div v-else class="success-msg">
          <p>{{ $t('followup_success_message') }}</p>
          <router-link to="/">
            <button class="alt-btn">{{ $t('back_home') }}</button>
          </router-link>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from '@/services/api'
export default {
  data() {
    return {
      form: {
        contact_info: '',
        location: '',
        description: ''
      },
      loading: false,
      success: false,
      errorMessage: ''
    };
  },
  methods: {
    async submitForm() {
        this.loading = true;
        this.errorMessage = '';
        try {
          const id = this.$route.params.id;
          const response = await axios.post(`/api/assessment/followup/${id}/`, this.form);

          
          this.success = true;  

        } catch (error) {
          // Get error message from backend or use fallback
          this.errorMessage = error.response?.data?.error || this.$t('followup_failed');
        } finally {
          this.loading = false;
        }
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
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: var(--bg-modal);
  border-radius: 20px;
  padding: 30px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
  animation: scaleIn 0.4s ease;
}
h2 {
  margin-top: 0;
  color: var(--primary-red);
  text-align: center;
}
.guide {
  margin: 10px 0;
  padding: 6px 10px;
  border-left: 4px solid var(--primary-red);
  background: var(--bg-guide);
  font-style: italic;
  font-size: 14px;
  color: var(--text-muted);
  border-radius: 8px;
}
.intro-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
}
.intro-form input,
.intro-form textarea {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid var(--border-input-auth);
  font-size: 16px;
  outline-color: var(--primary-red);
  resize: vertical;
  background: var(--bg-card);
  color: var(--text-dark);
}
.intro-form button {
  margin-top: 10px;
  padding: 12px;
  background-color: var(--primary-red);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}
.intro-form button:disabled {
  background-color: var(--accent-teal, #5eead4);
  cursor: not-allowed;
  opacity: 0.7;
}
.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 6px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  vertical-align: middle;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.actions {
  margin-top: 15px;
  text-align: center;
}
.alt-btn {
  background: var(--badge-bg);
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  color: var(--text-dark);
}
.success-msg {
  text-align: center;
  margin-top: 20px;
  font-size: 16px;
  background-color: var(--success-bg);
  padding: 15px;
  border-left: 5px solid var(--success-border);
  border-radius: 10px;
  color: var(--text-dark);
}
.error-msg {
  margin-top: 10px;
  color: var(--danger);
  font-size: 14px;
  text-align: center;
}
.modal-grow-enter-active,
.modal-grow-leave-active {
  transition: all 0.9s ease;
}
.modal-grow-enter-from,
.modal-grow-leave-to {
  opacity: 0;
  transform: scale(0.98);
}
@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
</style>

