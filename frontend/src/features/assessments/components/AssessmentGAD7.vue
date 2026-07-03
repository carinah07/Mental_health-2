<template>
  <div class="modal-overlay">
    <transition name="modal-grow" mode="out-in">
      <div class="modal">
        <h2>{{ $t('GAD7_title') }}</h2>

        <!-- Step 1: User Info -->
        <div v-if="step === 0" class="intro-form">
          <p class="guide">{{ $t('select_user_type') }}</p>
          <select v-model="formData.userType">
            <option disabled value="">{{ $t('choose_option') }}</option>
            <option value="self">{{ $t('self') }}</option>
            <option value="student">{{ $t('student') }}</option>
          </select>

          <p class="guide">{{ $t('select_age_group') }}</p>
          <select v-model="formData.ageGroup">
            <option disabled value="">{{ $t('choose_option') }}</option>
            <option value="5-10">5-10</option>
            <option value="11-15">11-15</option>
            <option value="16-20">16-20</option>
            <option value="21-25">21-25</option>
            <option value="26-30">26-30</option>
            <option value="31-35">31-35</option>
            <option value="36-40">36-40</option>
            <option value="40+">40+</option>
          </select>

          <p class="guide">{{ $t('select_sex') }}</p>
          <select v-model="formData.sex">
            <option disabled value="">{{ $t('choose_option') }}</option>
            <option value="male">{{ $t('male') }}</option>
            <option value="female">{{ $t('female') }}</option>
            
          </select>

          <button :disabled="!formComplete" @click="step = 1">{{ $t('start_assessment') }}</button>
        </div>

        <!-- Step 2: Questions -->
        <div v-else-if="step <= questions.length">
          <div class="progress-wrapper">
            <div class="progress-text">{{ step }} / {{ questions.length }}</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: (step / questions.length * 100) + '%' }"></div>
            </div>
          </div>

          <transition name="fade">
            <div class="question" v-if="step <= questions.length">
              <p class="guide">{{ $t('assessment_guide') }}</p>
              <p>{{ questions[step - 1].text }}</p>
              <div class="options">
                <button v-for="(option, index) in questions[step - 1].options" :key="index" @click="select(option.score)">
                  {{ option.text }}
                </button>
              </div>
            </div>
          </transition>
        </div>

        <!-- Step 3: Results -->
        <div class="result" v-if="step > questions.length">
          <p class="score">{{ $t('your_score') }}: {{ totalScore }} <i><b>{{ $t('out_of') }}</b></i> 21</p>

          <div v-if="loading" class="loading">
            ⏳ <span class="dots">{{ $t('janja_typing') }}</span>
          </div>

          <div v-else>
            <div v-if="aiMessageHTML" class="ai-response" v-html="aiMessageHTML"></div>

            <div v-if="redirectLink">
              <router-link :to="redirectLink">
                <button class="contact-btn">{{ $t('followup_support') }}</button>
              </router-link>
            </div>

            <div v-else>
              <p class="ai-response">{{ $t('use_akili') }}</p>
            </div>
          </div>
        </div>

        <!-- Close Button -->
        <div class="actions">
          <button :disabled="loading" @click="close">
            <span v-if="loading" class="spinner"></span>
            {{ $t('close') }}
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { marked } from "marked";
import axios from '@/services/api'

export default {
  emits: ["close"],
  data() {
    return {
      step: 0,
      totalScore: 0,
      loading: false,
      aiMessage: "",
      aiMessageHTML: "",
      redirectLink: null,
      scores: [],
      formData: {
        userType: "",
        ageGroup: "",
        sex: ""
      },
      questions: Array.from({ length: 7 }, (_, i) => ({
        text: this.$t(`GAD-7_${i + 1}`),
        options: this.opts()
      }))
    };
  },
  computed: {
    formComplete() {
      return this.formData.userType && this.formData.ageGroup && this.formData.sex;
    }
  },
  methods: {
    opts() {
      return [
        { text: this.$t('PHQ-Option_1'), score: 0 },
        { text: this.$t('PHQ-Option_2'), score: 1 },
        { text: this.$t('PHQ-Option_3'), score: 2 },
        { text: this.$t('PHQ-Option_4'), score: 3 },
      ];
    },
    async select(score) {
      this.scores.push(score);
      this.totalScore += score;
      this.step++;

      if (this.step > this.questions.length) {
        await this.getAIResponse();
      }
    },
    async getAIResponse() {
      this.loading = true;
      try {
        const lang_sample = this.questions[0].text;
        const res = await axios.post("/api/assessment/gad7/", {
            scores: this.scores,
            lang_text: lang_sample,
            user_type: this.formData.userType,
            age_group: this.formData.ageGroup,
            sex: this.formData.sex,
        });

        const data = res.data;
        this.aiMessage = data.response || "*Could not retrieve AI insight.*";
        this.aiMessageHTML = marked.parse(this.aiMessage);
        this.redirectLink = data.redirect_link || null; // e.g., "/followup/abc123"

      } catch (err) {
        this.aiMessage = "*Network issue. Try again later.*";
        this.aiMessageHTML = marked.parse(this.aiMessage);
      } finally {
        this.loading = false;
      }
    },
    close() {
      if (!this.loading) this.$emit("close");
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
.progress-wrapper {
  margin-bottom: 1.5rem;
}
.progress-text {
  text-align: center;
  font-weight: bold;
}
.progress-bar {
  background-color: var(--border-input);
  border-radius: 10px;
  height: 12px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background-color: var(--primary-red);
  transition: width 0.3s ease;
}
b {
  color: var(--text-dark);
  font-size: 14px;
}
.question p {
  font-size: 17px;
  font-weight: 600;
  margin-bottom: 1rem;
}
.question .guide {
  margin: 3px 0;
  padding: 3px 6px;
  border-left: 4px solid var(--primary-red);
  background: var(--bg-guide);
  font-style: italic;
  font-size: 14px;
  color: var(--text-muted);
  border-radius: 8px;
}
.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.options button {
  background-color: var(--bg-guide);
  border: 1px solid var(--primary-red);
  padding: 10px 15px;
  border-radius: 12px;
  cursor: pointer;
  color: var(--text-dark);
}
.options button:hover {
  background-color: var(--primary-red);
  color: white;
}
.result p {
  font-size: 1rem;
  text-align: center;
}
.score {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-red);
  margin-bottom: 1rem;
}
.recomendations {
  margin: 6px auto;
  padding: 10px 15px;
  font-size: 15px;
  border-radius: 10px;
  width: 90%;
  text-align: center;
}
.good {
  background-color: #d6f5d6;
  border-left: 5px solid green;
}
.average {
  background-color: #fff8e1;
  border-left: 5px solid orange;
}
.bad {
  background-color: #e6fff9;
  border-left: 5px solid red;
}
.loading {
  text-align: center;
  font-style: italic;
  color: var(--text-muted);
  margin-top: 15px;
  font-size: 15px;
}
.dots::after {
  content: '...';
  animation: dotFlash 1.5s steps(3, end) infinite;
}
@keyframes dotFlash {
  0% { content: ''; }
  33% { content: '.'; }
  66% { content: '..'; }
  100% { content: '...'; }
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
.ai-response {
  text-align: center;
  margin-top: 15px;
  padding: 10px;
  border-left: 4px solid var(--text-muted);
  background: var(--bg-card);
  border-radius: 8px;
}
.actions {
  text-align: center;
  margin-top: 20px;
}
.actions button {
  padding: 10px 20px;
  background-color: var(--primary-red);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
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
.actions button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
.intro-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}

.intro-form select {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid var(--border-input-auth);
  font-size: 16px;
  background: var(--bg-card);
  color: var(--text-dark);
  outline-color: var(--primary-red);
}

.intro-form button {
  margin-top: 15px;
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

.intro-form button:disabled {
  background-color: var(--accent-teal, #5eead4);
  cursor: not-allowed;
  opacity: 0.7;
}

.contact-btn {
  margin-top: 15px;
  padding: 12px 20px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.contact-btn:hover {
  background-color: #1a252f;
}

</style>


