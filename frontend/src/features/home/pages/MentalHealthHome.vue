<template>
  <div class="container">
    <header class="navbar" :class="{ open: menuOpen }">
      <div class="nav-left">
        <!-- MindCare SVG Logo -->
        <svg class="nav-logo" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="24" cy="24" r="22" fill="#e6fff9" stroke="#0d9488" stroke-width="2"/>
          <path d="M16 20c0-4.4 3.6-8 8-8s8 3.6 8 8c0 3-1.6 5.6-4 7.1V32h-8v-4.9C17.6 25.6 16 23 16 20z" stroke="#0d9488" stroke-width="2" stroke-linejoin="round" fill="none"/>
          <path d="M20 32h8" stroke="#0d9488" stroke-width="2" stroke-linecap="round"/>
          <path d="M21 35h6" stroke="#0d9488" stroke-width="2" stroke-linecap="round"/>
          <path d="M20 20c0-2.2 1.8-4 4-4" stroke="#5eead4" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <h2 class="brand-name">MindCare</h2>
      </div>

      <div class="hamburger" @click="toggleMenu">
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
        <span :class="{ open: menuOpen }"></span>
      </div>

      <nav class="nav-links" :class="{ show: menuOpen }">
        <a @click="$router.push('/')" class="nav-link">Home</a>
        <a><LanguageSelector /></a>
      </nav>
    </header>

    <h1 class="heading">{{ $t('title') }}</h1>
    <p class="sub">{{ $t('welcome') }}</p>

    <div class="grid">
      <!-- Assessment Card -->
      <DashboardCard :title="$t('assessment_title')" :description="$t('PHQ9_description')" @click="modal = 'assessment'">
        <template #icon>
          <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="10" y="6" width="36" height="44" rx="4" stroke="#0d9488" stroke-width="2.5"/>
            <rect x="18" y="2" width="20" height="8" rx="3" stroke="#0d9488" stroke-width="2" fill="#e6fff9"/>
            <line x1="18" y1="22" x2="38" y2="22" stroke="#0d9488" stroke-width="2" stroke-linecap="round"/>
            <line x1="18" y1="30" x2="38" y2="30" stroke="#0d9488" stroke-width="2" stroke-linecap="round"/>
            <line x1="18" y1="38" x2="30" y2="38" stroke="#0d9488" stroke-width="2" stroke-linecap="round"/>
            <circle cx="42" cy="42" r="8" fill="#0d9488"/>
            <path d="M38.5 42l2.5 2.5 4-4" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </template>
      </DashboardCard>

      <!-- Chat with Mia Card -->
      <DashboardCard :title="$t('nlp_chat')" :description="$t('nlp_description')" @click="openNLPModal">
        <template #icon>
          <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="8" width="40" height="30" rx="6" stroke="#0d9488" stroke-width="2.5"/>
            <path d="M4 48l8-10h32" stroke="#0d9488" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M24 19c0-2.8 3.6-4.4 5.5-2.1 1.9-2.3 5.5-.7 5.5 2.1 0 1.5-.8 2.8-2 3.6L29.5 26 24 22.6c-1.2-.8-2-2.1-2-3.6z" fill="#0d9488" opacity="0.8"/>
          </svg>
        </template>
      </DashboardCard>

      <!-- Education Card -->
      <DashboardCard :title="$t('rule_chat')" :description="$t('rule_description')" @click="modal = 'rule'">
        <template #icon>
          <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M28 10L6 20l22 10 22-10-22-10z" stroke="#0d9488" stroke-width="2.5" stroke-linejoin="round"/>
            <path d="M6 20v16" stroke="#0d9488" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M14 24v10c0 3.3 6.3 6 14 6s14-2.7 14-6V24" stroke="#0d9488" stroke-width="2.5" stroke-linecap="round"/>
            <circle cx="46" cy="24" r="3" fill="#5eead4"/>
          </svg>
        </template>
      </DashboardCard>

      <!-- Find Experts Card -->
      <DashboardCard :title="$t('experts')" :description="$t('experts_description')" @click="modal = 'experts'">
        <template #icon>
          <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="22" cy="18" r="9" stroke="#0d9488" stroke-width="2.5"/>
            <path d="M4 46c0-9.9 8.1-18 18-18" stroke="#0d9488" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M40 28c4.4 0 8 3.6 8 8 0 5.5-8 14-8 14S32 41.5 32 36c0-4.4 3.6-8 8-8z" stroke="#0d9488" stroke-width="2.5" fill="#e6fff9"/>
            <circle cx="40" cy="36" r="3" fill="#0d9488"/>
          </svg>
        </template>
      </DashboardCard>
    </div>

    <!-- Modals -->
    <transition name="bot-modal">
      <NLPChatModal v-if="modal === 'nlp'" @close="modal = null" />
    </transition>
    <AssessmentModal v-if="modal === 'assessment'" @close="modal = null" />
    <AssessmentGAD7 v-if="modal === 'assessmentGAD7'" @close="modal = null" />
    <RuleChatModal v-if="modal === 'rule'" @close="modal = null" />
    <ExpertsModal v-if="modal === 'experts'" @close="modal = null" />

    <!-- Floating Bot (Mia) -->
    <div class="floating-bot" @click="openNLPModal">
      <div class="tooltip">
        <strong>{{ $t('nlp_chat') }}</strong><br />
        <small>{{ $t('nlp2_description') }}</small>
      </div>
      <svg class="bot-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="52" height="52">
        <circle cx="32" cy="32" r="30" fill="#0d9488"/>
        <path d="M24 26c-2.2 0-4 1.8-4 4s1.8 4 4 4 4-1.8 4-4-1.8-4-4-4zm16 0c-2.2 0-4 1.8-4 4s1.8 4 4 4 4-1.8 4-4-1.8-4-4-4z" fill="#fff"/>
        <path d="M32 44c4 0 7.5-2.5 8.7-6H23.3c1.2 3.5 4.7 6 8.7 6z" fill="#fff"/>
      </svg>
    </div>

    <div class="footer">
      <small>&copy; {{ new Date().getFullYear() }} MindCare. Final Year Project.</small>
    </div>
  </div>
</template>

<script>
import LanguageSelector from "@/shared/components/LanguageSelector.vue";
import DashboardCard from "@/shared/components/DashboardCard.vue";
import AssessmentModal from "@/features/assessments/components/AssessmentModal.vue";
import AssessmentModal2 from "@/features/assessments/components/AssessmentModal2.vue";
import AssessmentGAD7 from "@/features/assessments/components/AssessmentGAD7.vue";
import NLPChatModal from "@/features/chat/components/NLPChatModal.vue";
import RuleChatModal from "@/features/chat/components/RuleChatModal.vue";
import ExpertsModal from "@/features/experts/components/ExpertsModal.vue";

export default {
  components: {
    LanguageSelector,
    DashboardCard,
    AssessmentModal,
    AssessmentModal2,
    AssessmentGAD7,
    NLPChatModal,
    RuleChatModal,
    ExpertsModal,
  },
  data() {
    return {
      modal: null,
      botSound: null,
      menuOpen: false,
    };
  },
  mounted() {
    this.botSound = new Audio('/sounds/bot-open.mp3');
  },
  methods: {
    openNLPModal() {
      this.modal = 'nlp';
      if (this.botSound) {
        this.botSound.currentTime = 0;
        this.botSound.play().catch(() => {});
      }
    },
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },
  },
};
</script>

<style scoped>
.container {
  padding: 1rem 2rem;
  max-width: 100%;
  margin: auto;
  position: relative;
}

.navbar {
  background: linear-gradient(135deg, #e6fff9, #f0fdfa);
  color: var(--primary-teal);
  padding: 1rem 2rem;
  border-radius: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  box-shadow: 0 4px 16px rgba(13, 148, 136, 0.15);
  margin-bottom: 2rem;
  border-bottom: 2px solid #5eead4;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-logo {
  width: 46px;
  height: 46px;
}

.brand-name {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--primary-teal);
  letter-spacing: -0.5px;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  transition: all 0.3s ease-in-out;
}

.nav-link {
  color: var(--primary-teal);
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.nav-link:hover {
  background-color: #ccfbf1;
}

.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  cursor: pointer;
}

.hamburger span {
  width: 26px;
  height: 3px;
  background-color: var(--primary-teal);
  border-radius: 2px;
  transition: all 0.3s ease-in-out;
}

.hamburger span.open:nth-child(1) { transform: rotate(45deg) translate(6px, 7px); }
.hamburger span.open:nth-child(2) { opacity: 0; }
.hamburger span.open:nth-child(3) { transform: rotate(-45deg) translate(4px, -5px); }

@media (max-width: 768px) {
  .nav-links { flex-direction: column; width: 100%; margin-top: 1rem; display: none; }
  .nav-links.show { display: flex; }
  .hamburger { display: flex; }
}

.heading {
  text-align: center;
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--primary-teal);
  margin-bottom: 0.4rem;
}
.sub {
  text-align: center;
  color: #555;
  margin-bottom: 2rem;
}
.grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.grid > * {
  height: 190px;
  width: 85%;
  max-width: 380px;
}

.footer {
  text-align: center;
  margin-top: 2.5rem;
  color: #777;
  font-size: 0.85rem;
}

/* Floating Bot */
.floating-bot {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 999;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  animation: wave 2.5s infinite ease-in-out;
}

.floating-bot:hover { transform: translateY(-4px); }

.bot-icon {
  border-radius: 50%;
  box-shadow: 0 4px 16px rgba(13, 148, 136, 0.4);
  transition: transform 0.2s ease;
}

.bot-icon:hover { transform: scale(1.07); }

.tooltip {
  background: white;
  color: #333;
  padding: 0.6rem 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  position: absolute;
  right: 64px;
  bottom: 10px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transform: translateX(10px);
  transition: all 0.3s ease;
  border-left: 3px solid var(--primary-teal);
}

.floating-bot:hover .tooltip {
  opacity: 1;
  transform: translateX(0);
  pointer-events: auto;
}

@keyframes wave {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}
</style>
