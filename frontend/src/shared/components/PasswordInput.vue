<template>
  <div class="password-field">
    <input
      :id="inputId"
      :type="visible ? 'text' : 'password'"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :minlength="minlength"
      :autocomplete="autocomplete"
      @input="$emit('update:modelValue', $event.target.value)"
    />
    <button
      type="button"
      class="toggle-btn"
      :aria-label="visible ? $t('hide_password') : $t('show_password')"
      @click="visible = !visible"
    >
      <svg v-if="visible" width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M3 3l18 18M10.58 10.58A2 2 0 0012 15a2 2 0 001.42-.58M9.88 4.24A10.94 10.94 0 0112 5c5 0 9.27 3.11 11 7-1.02 2.28-2.78 4.18-5 5.32M6.11 6.11C4.18 7.45 2.73 9.34 1.73 11.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
      <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z" stroke="currentColor" stroke-width="2"/>
        <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  modelValue: { type: String, default: '' },
  inputId: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  required: { type: Boolean, default: false },
  minlength: { type: [String, Number], default: undefined },
  autocomplete: { type: String, default: 'current-password' },
})

defineEmits(['update:modelValue'])

const visible = ref(false)
</script>

<style scoped>
.password-field {
  position: relative;
  display: flex;
  align-items: center;
}

input {
  width: 100%;
  padding: 0.75rem 2.75rem 0.75rem 1rem;
  border: 1px solid var(--border-input);
  border-radius: 10px;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  background: var(--bg-card);
  color: var(--text-dark);
}

.toggle-btn {
  position: absolute;
  right: 0.6rem;
  top: 50%;
  transform: translateY(calc(-50% - 0.25rem));
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border: none;
  background: transparent;
  color: var(--primary-teal);
  cursor: pointer;
  border-radius: 6px;
  padding: 0;
}

.toggle-btn:hover {
  background: var(--bg-hover-teal);
}
</style>
