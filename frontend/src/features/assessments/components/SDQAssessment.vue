<template>
  <div>
    <h2>{{ $t('child_title') }}</h2>
    <p class="child-desc">{{ $t('child_description') }}</p>
    <!-- Step 0: Age & Sex -->
    <div v-if="step === 0" class="intro-form">
      

      <p class="guide">{{ $t('select_age_group_child') }}</p>
      <select v-model="form.ageGroup">
        <option disabled value="">{{ $t('choose_option') }}</option>
        <option value="4-7">4–7</option>
        <option value="8-12">8–12</option>
        <option value="13-17">13–17</option>
      </select>

      <p class="guide">{{ $t('select_sex_child') }}</p>
      <select v-model="form.sex">
        <option disabled value="">{{ $t('choose_option') }}</option>
        <option value="male">{{ $t('male') }}</option>
        <option value="female">{{ $t('female') }}</option>
      </select>

      <button :disabled="!formComplete" @click="startAssessment">
        {{ $t('start_assessment') }}
      </button>
    </div>

    <!-- Questions -->
    <div v-else-if="step > 0 && step <= questions.length" class="question-form">
        <div class="progress-wrapper">
        <div class="progress-text">{{ step }} / {{ questions.length }}</div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
      </div>
      <p class="guide">{{ $t('assessment_guide_child') }}</p>
  <transition name="fade-slide" mode="out-in">
    <div class="animated-question" :key="step">
      
      <p>{{ questions[step - 1].text }}</p>
      <div class="options">
        <button
          v-for="opt in questions[step - 1].options"
          :key="opt.value"
          @click="select(opt.value)"
        >
          {{ $t(opt.label) }}
        </button>
      </div>
    </div>
  </transition>
</div>

    <!-- Results -->
    <div v-else class="result">
      <p class="score">{{ $t('child_score') }}: {{ totalScore }} <b>{{ $t('out_of') }}</b> 50</p>
     <table class="score-table">
        <tbody>
          <tr>
            <td>{{ $t('sdq_difficulties') }}</td>
            <td>{{ difficultiesScore }}</td>
          </tr>
          <tr>
            <td>{{ $t('sdq_prosocial') }}</td>
            <td>{{ prosocialScore }}</td>
          </tr>
        </tbody>
      </table>

       <div v-if="showScrollArrow" class="scroll-arrow">⬇</div>
      <div v-if="loading" class="loading">⏳ <span class="dots">{{ $t('janja_typing') }}</span></div>
      <div v-else>
        <div class="ai-response" v-if="aiMessageHTML" v-html="aiMessageHTML"  ref="aiContainer" @scroll="handleScroll"></div>
        <router-link v-if="redirectLink" :to="redirectLink">
          <button class="contact-btn">{{ $t('followup_support') }}</button>
        </router-link>

       
      </div>
    </div>

    <!-- Close -->
    <div class="actions">
      <button :disabled="loading" @click="handleClose">
        <span v-if="loading" class="spinner" />
        {{ $t('close') }}
      </button>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';
import axios from '@/services/api'

const RAW_QUESTIONS = [
  'SDQ_1', 'SDQ_2', 'SDQ_3', 'SDQ_4', 'SDQ_5',
  'SDQ_6', 'SDQ_7', 'SDQ_8', 'SDQ_9', 'SDQ_10',
  'SDQ_11', 'SDQ_12', 'SDQ_13', 'SDQ_14', 'SDQ_15',
  'SDQ_16', 'SDQ_17', 'SDQ_18', 'SDQ_19', 'SDQ_20',
  'SDQ_21', 'SDQ_22', 'SDQ_23', 'SDQ_24', 'SDQ_25',
];

const SUBSCALES = ['emotional', 'emotional', 'emotional', 'emotional', 'emotional',
  'conduct', 'conduct', 'conduct', 'conduct', 'conduct',
  'hyper', 'hyper', 'hyper', 'hyper', 'hyper',
  'peer', 'peer', 'peer', 'peer', 'peer',
  'prosocial', 'prosocial', 'prosocial', 'prosocial', 'prosocial'];

export default {
  emits: ['close'],
  data() {
    return {
      step: 0,
      form: { ageGroup: '', sex: '', userType: 'child' },
      questions: [],
      responses: [],
      totalScore: 0,
      difficultiesScore: 0,
      prosocialScore: 0,
      loading: false,
      aiMessageHTML: '',
      redirectLink: '',
      showScrollArrow: false
    };
  },
  computed: {
    formComplete() {
      return this.form.ageGroup && this.form.sex;
    },
    progress() {
      return (this.step / this.questions.length) * 100;
    }
  },mounted() {
  this.$nextTick(() => {
    this.checkScroll();
  });
},
watch: {
  aiMessageHTML() {
    this.$nextTick(() => {
      setTimeout(() => {
        this.checkScroll();
      }, 50);
    });
  }
},
methods: {
  checkScroll() {
    const container = this.$refs.aiContainer;
    if (!container) return;
    const shouldShow =
      container.scrollHeight > container.clientHeight &&
      container.scrollTop + container.clientHeight < container.scrollHeight;
    this.showScrollArrow = shouldShow;
  },
  handleScroll() {
    const container = this.$refs.aiContainer;
    if (!container) return;
    const nearBottom =
      container.scrollTop + container.clientHeight >= container.scrollHeight - 5;
    this.showScrollArrow = !nearBottom;
  },
    startAssessment() {
      const opts = [
        { label: 'response_not', value: 0 },
        { label: 'response_some', value: 1 },
        { label: 'response_certain', value: 2 }
      ];

      // Translate SDQ questions using $t dynamically here
      this.questions = RAW_QUESTIONS.map((key, i) => ({
        text: this.$t(key),
        subscale: SUBSCALES[i],
        options: opts
      }));

      this.step = 1;
    },
    async select(score) {
      const current = this.questions[this.step - 1];

      this.responses.push({
        question: current.text,
        score,
        subscale: current.subscale
      });

      this.totalScore += score;
      this.step++;

      if (this.step > this.questions.length) {
        await this.submit();
      }
    },
    async submit() {
  this.loading = true;
        try {
          const res = await axios.post(`/api/assessment/sdq/`, {
              responses: this.responses,
              difficulties: this.responses
                .filter(r => ['emotional', 'conduct', 'hyper', 'peer'].includes(r.subscale))
                .reduce((sum, r) => sum + r.score, 0),
              prosocial: this.responses
                .filter(r => r.subscale === 'prosocial')
                .reduce((sum, r) => sum + r.score, 0),
              scores: this.responses.map(r => r.score),
              lang_text: this.questions[0].text,
              user_type: 'child',
              age_group: this.form.ageGroup,
              sex: this.form.sex
          });

          const data = res.data;

          // Calculate SDQ subscores
          this.difficultiesScore = this.responses
            .filter(r => ['emotional', 'conduct', 'hyper', 'peer'].includes(r.subscale))
            .reduce((sum, r) => sum + r.score, 0);

          this.prosocialScore = this.responses
            .filter(r => r.subscale === 'prosocial')
            .reduce((sum, r) => sum + r.score, 0);

          this.aiMessageHTML = marked.parse(data.response || '*No feedback available.*');
          this.redirectLink = data.redirect_link || null;

        } catch (err) {
          this.aiMessageHTML = marked.parse('*Network error. Please try again later.*');
        } finally {
          this.loading = false;
        }
      },

    handleClose() {
      if (!this.loading) this.$emit('close');
    }
  }
};
</script>


<style scoped>
h2 {
  margin-top: 0;
  color: var(--primary-red);
  text-align: center;
}
b {
  color: black;
  font-size: 14px;
}
.progress-wrapper {
  margin-bottom: 1.5rem;
}
.progress-text {
  text-align: center;
  font-weight: bold;
}
.progress-bar {
  background-color: #99f6e4;
  border-radius: 10px;
  height: 12px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background-color: var(--primary-red);
  transition: width 0.3s ease;
}
.child-desc {
    text-align: center;
    font-style: italic;
}
.question p {
  font-size: 17px;
  font-weight: 600;
  margin-bottom: 1rem;
}
.guide {
  margin: 3px 0;
  padding: 3px 6px;
  border-left: 4px solid var(--primary-red);
  background: #f0fdfa;
  font-style: italic;
  font-size: 14px;
  color: #555;
  border-radius: 8px;
}
.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.options button {
  background-color: #f0fdfa;
  border: 1px solid var(--primary-red);
  padding: 10px 15px;
  border-radius: 12px;
  cursor: pointer;
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
  color: #555;
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
.score-table {
  margin: 20px auto;
  width: 90%;
  max-width: 400px;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  font-size: 16px;
  background-color: #f0fdfa;
  color: #333;
}

.score-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #a7f3d0;
}

.score-table tr:last-child td {
  border-bottom: none;
}

.score-table td:first-child {
  font-weight: bold;
  color: var(--primary-red);
  background-color: #e6fff9;
}

.score-table td:last-child {
  text-align: right;
  font-weight: bold;
}

.ai-response {
  max-height: 250px;
  overflow-y: auto;
  margin-top: 15px;
  padding: 10px;
  border-left: 4px solid var(--primary-red);
  position: relative;
  background-color: var(--light-pink);
  border-radius: 8px;
}
.result {
  position: relative;
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
  border: 1px solid #ccc;
  font-size: 16px;
  background: #fff;
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
  background-color: #5eead4;
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

.slide-fade-enter-active {
  transition: opacity 0.5s ease-out, transform 0.5s ease-out;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
.scroll-arrow {
  position: absolute;
  bottom: 30px;
  right: 30px;
  font-size: 2rem;
  color: var(--primary-red);
  animation: bounce 1.5s infinite;
  z-index: 9999;
  background: white;
  padding: 8px 12px;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  pointer-events: none;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(8px);
  }
}

</style>

