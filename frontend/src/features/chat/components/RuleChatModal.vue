<template>
  <div class="modal-overlay">
    <div class="modal">
      <div class="header">
        <div class="modal-brand">
          <svg width="36" height="36" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="24" cy="24" r="22" fill="#e6fff9" stroke="#0d9488" stroke-width="2"/>
            <path d="M24 12L10 20l14 8 14-8-14-8z" stroke="#0d9488" stroke-width="2" stroke-linejoin="round" fill="none"/>
            <path d="M10 20v10c0 3.3 6.3 6 14 6s14-2.7 14-6V20" stroke="#0d9488" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span class="brand-label">Learn</span>
        </div>
        <div class="header-buttons">
          <button class="reset-btn" @click="startNewChat">New Chat</button>
          <button class="close-btn" @click="$emit('close')">×</button>
        </div>
      </div>

      <!-- Chat container -->
      <div class="chat-body" ref="chatBody">
        <div class="messages">
          <!-- Initial system message -->
          <div v-if="stack.length === 0" class="message bot fade">
            <div class="bubble bot-bubble">
              {{ $t('select_section') }}
              <div class="options">
                <button
                  v-for="type in nodeTypes"
                  :key="type.key"
                  @click="loadRoot(type.key)"
                >
                  {{ $t(type.labelKey) }}
                </button>
              </div>
            </div>
          </div>

          <!-- Chat history -->
          <div v-for="(step, i) in history" :key="i">
            <div class="message user fade">
              <div class="bubble user-bubble">{{ step.title }}</div>
            </div>
            <div class="message bot fade">
              <div class="bubble bot-bubble">
                <p v-if="step.content">{{ step.content }}</p>
                <div class="options" v-if="step.children && step.children.length">
                  <button
                    v-for="child in step.children"
                    :key="child.id"
                    @click="loadChildren(child)"
                  >
                    {{ child[`title_${lang}`] }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom action bar -->
      <div class="actions">
        <button class="back-btn" v-if="stack.length > 0 || loading" @click="goBack" :disabled="loading">
          <span v-if="loading" class="dots-loader">
            <span></span><span></span><span></span>
          </span>
          <span v-else>← {{ $t('back') }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/services/api';

export default {
  emits: ["close"],
  data() {
    return {
      lang: this.$i18n.locale || "en",
      stack: [],
      history: [],
      loading: false,
      nodeTypes: [
        { key: "user", labelKey: "for_users" },
        { key: "teacher", labelKey: "for_teachers" },
        { key: "parent", labelKey: "for_parents" },
      ],
    };
  },
  methods: {
    async loadRoot(type) {
      this.stack = [];
      this.history = [];
      this.loading = true;
      const res = await axios.get(`/api/education/content/roots/?type=${type}`);
      const data = res.data;

      if (data.length) {
        const root = data[0];
        const childrenRes = await axios.get(`/api/education/content/${root.id}/children/`);
        const children = childrenRes.data;

        this.stack.push(root.id);
        this.history.push({
          title: root[`title_${this.lang}`],
          content: root[`content_${this.lang}`],
          children,
        });
      }
      this.loading = false;
      this.scrollToBottom();
    },

    async loadChildren(node) {
      this.loading = true;
      const childrenRes = await axios.get(`/api/education/content/${node.id}/children/`);
      const children = childrenRes.data;

      this.stack.push(node.id);
      this.history.push({
        title: node[`title_${this.lang}`],
        content: node[`content_${this.lang}`],
        children,
      });
      this.loading = false;
      this.scrollToBottom();
    },

    async goBack() {
      this.loading = true;
      await new Promise((resolve) => setTimeout(resolve, 400)); // simulate delay
      this.stack.pop();
      this.history.pop();
      this.loading = false;
      this.scrollToBottom();
    },

    startNewChat() {
      this.stack = [];
      this.history = [];
      this.scrollToBottom();
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const chat = this.$refs.chatBody;
        if (chat) {
          chat.scrollTo({
            top: chat.scrollHeight,
            behavior: "smooth",
          });
        }
      });
    },
  },
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
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.modal {
  background: #fff;
  border-radius: 16px;
  width: 90%;
  max-width: 500px;
  height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.4s ease;
  overflow: hidden;
  position: relative;
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
.brand-label {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--primary-teal);
}

.header-buttons {
  display: flex;
  gap: 5px;
}

.close-btn,
.reset-btn {
  background: transparent;
  border: none;
  font-size: 1.2rem;
  color: var(--primary-teal);
  cursor: pointer;
  padding: 0.2rem 0.6rem;
  border-radius: 8px;
  transition: background 0.2s ease;
}

.reset-btn {
  background: var(--primary-teal);
  color: white;
}
.close-btn {
  background: white;
  border: 1px solid var(--primary-teal);
  color: var(--primary-teal);
}
.reset-btn:hover,
.close-btn:hover {
  background: white;
  border: 1px solid var(--primary-teal);
  color: var(--primary-teal);
}

.chat-body {
  flex-grow: 1;
  background: #f7f7f7;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  scroll-behavior: smooth;
}

.messages {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message {
  display: flex;
}
.message.user {
  justify-content: flex-end;
}
.message.bot {
  justify-content: flex-start;
}

.bubble {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 16px;
  line-height: 1.5;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  font-size: 14px;
}
.user-bubble {
  background: #d9fdd3;
  align-self: flex-end;
  border-bottom-right-radius: 0;
}
.bot-bubble {
  background: #ffffff;
  border-left: 4px solid var(--primary-teal);
  border-bottom-left-radius: 0;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 1rem;
}
.options button {
  padding: 10px;
  background: var(--primary-teal);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  text-align: left;
}
.options button:hover {
  background-color: var(--primary-teal-dark);
}

.actions {
  padding: 0.8rem;
  background: #fff;
  border-top: 1px solid #eee;
  text-align: center;
}

.back-btn {
  background: #eee;
  color: #333;
  border: none;
  padding: 8px 20px;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  font-size: 15px;
}
.back-btn:disabled {
  cursor: not-allowed;
  opacity: 0.8;
}
.back-btn:hover:not(:disabled) {
  background-color: #ddd;
}

/* Dot Loader inside back button */
.dots-loader {
  display: flex;
  align-items: center;
  gap: 4px;
  justify-content: center;
}
.dots-loader span {
  width: 6px;
  height: 6px;
  background: var(--primary-teal);
  border-radius: 50%;
  animation: bounce 1s infinite;
}
.dots-loader span:nth-child(2) {
  animation-delay: 0.2s;
}
.dots-loader span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.6;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from { transform: translateY(40px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
