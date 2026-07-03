<!-- AssessmentSelector.vue -->
<template>
  <div class="modal-overlay">
    <transition name="modal-grow" mode="out-in">
      <div class="modal">
        <h2 v-if="!selected">{{ $t('choose_assessment') }}</h2>

        <div v-if="!selected" class="intro-form">
          <p class="guide">{{ $t('select_assessment_type') }}</p>
          <button @click="selected = 'phq9'">{{ $t('depression_assessment') }}</button>
          <button @click="selected = 'gad7'">{{ $t('anxiety_assessment') }}</button>
          <button @click="selected = 'sdq'">{{ $t('assess_child') }}</button>

          <!-- Close Button -->
      <div class="actions">
        <button :disabled="loading" @click="handleClose">
          <span v-if="loading" class="spinner" />
          {{ $t('close') }}
        </button>
    </div>
        </div>

        <!-- Dynamic Component -->
        <transition name="fade" mode="out-in">
          <component
            :is="selectedComponent"
            v-if="selected"
            @close="handleClose"
          />
        </transition>
      </div>
    </transition>
  </div>
</template>

<script>
import PHQ9Assessment from './PHQ9Assessment.vue'
import GAD7Assessment from './GAD7Assessment.vue'
import SDQAssessment from './SDQAssessment.vue'

export default {
  emits: ['close'],
  components: { PHQ9Assessment, GAD7Assessment, SDQAssessment },
  data() {
    return {
      selected: null
    }
  },
  computed: {
    selectedComponent() {
      return {
        phq9: 'PHQ9Assessment',
        gad7: 'GAD7Assessment',
        sdq: 'SDQAssessment'
      }[this.selected]
    }
  },
  methods: {
    handleClose() {
      this.selected = null // reset selection
      this.$emit('close')
    }
  }
}
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
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 10px 20px rgba(0,0,0,0.15);
  animation: scaleIn 0.4s ease;
}

h2 {
  margin-top: 0;
  color: var(--primary-red);
  text-align: center;
}

.intro-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
}

.intro-form .guide {
  margin: 3px 0;
  padding: 3px 6px;
  border-left: 4px solid var(--primary-red);
  background: var(--bg-guide);
  font-style: italic;
  font-size: 14px;
  color: var(--text-muted);
  border-radius: 8px;
}

.intro-form button {
  padding: 12px;
  background-color: var(--primary-red);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.intro-form button:hover {
  background-color: #0f766e;
}
.actions {
  text-align: center;
  margin-top: 20px;
}
.actions button {
  padding: 10px 20px;
  background-color: var(--bg-card);
  color: var(--primary-red);
  border: 1px solid var(--primary-red);
  border-radius: 10px;
  cursor: pointer;
}
.actions button:hover {
  background-color: var(--primary-red);
  color: white;
  border: none;
  
}

/* Modal and fade animations */
.modal-grow-enter-active,
.modal-grow-leave-active {
  transition: all 0.9s ease;
}
.modal-grow-enter-from,
.modal-grow-leave-to {
  opacity: 0;
  transform: scale(0.98);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
</style>


