<template>
  <div ref="bgRef" class="floating-bg" @mousemove="onMouseMove">
    <div
      v-for="(item, i) in items"
      :key="i"
      class="floating-item"
    >
      <div
        class="floating-inner"
        :style="{ width: item.size + 'px', height: item.size + 'px', color: '#0d9488', opacity: item.opacity }"
        v-html="item.svg"
      ></div>
    </div>
  </div>
  <div class="background-glow"></div>
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
        <a @click="$router.push('/my-reports')" class="nav-link">{{ $t('my_reports') }}</a>
        <a v-if="auth.isAdmin" @click="$router.push('/admin')" class="nav-link">{{ $t('admin_panel') }}</a>
        <a @click="handleLogout" class="nav-link">{{ $t('logout') }}</a>
        <a><LanguageSelector /></a>
        <ThemeToggle />
      </nav>
    </header>

    <h1 class="heading">{{ $t('welcome_user') }}, {{ auth.displayName }}</h1>
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

    </div>

    <!-- Modals -->
    <transition name="bot-modal">
      <NLPChatModal v-if="modal === 'nlp'" @close="modal = null" />
    </transition>
    <AssessmentModal v-if="modal === 'assessment'" @close="modal = null" />
    <AssessmentGAD7 v-if="modal === 'assessmentGAD7'" @close="modal = null" />
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
import ThemeToggle from "@/shared/components/ThemeToggle.vue";
import LanguageSelector from "@/shared/components/LanguageSelector.vue";
import DashboardCard from "@/shared/components/DashboardCard.vue";
import AssessmentModal from "@/features/assessments/components/AssessmentModal.vue";
import AssessmentGAD7 from "@/features/assessments/components/AssessmentGAD7.vue";
import NLPChatModal from "@/features/chat/components/NLPChatModal.vue";
import { useAuthStore } from "@/stores/auth";

const iconSvgs = [
  // Brain
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M24 6C15.7 6 9 12.7 9 21c0 5.2 2.8 9.7 7 12.2V42h16V33.2C36.2 30.7 39 26.2 39 21c0-8.3-6.7-15-15-15z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M17 42h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M19 46h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M20 21c0-2.2 1.8-4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
  // Heart
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M24 42s-16-10-16-22c0-6 4-10 10-10 3.5 0 6 2 6 2s2.5-2 6-2c6 0 10 4 10 10 0 12-16 22-16 22z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
  // Plus/Cross
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="6" width="8" height="36" rx="2" fill="currentColor" opacity="0.6"/><rect x="6" y="20" width="36" height="8" rx="2" fill="currentColor" opacity="0.6"/></svg>',
  // Puzzle piece
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 10h12v6c-2 0-4 2-4 4s2 4 4 4v6H10V10z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="20" cy="20" r="2" fill="currentColor" opacity="0.4"/></svg>',
  // Thought bubble
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8 20c0-7.7 7.2-14 16-14s16 6.3 16 14-7.2 14-16 14c-2.5 0-4.8-.5-6.9-1.3L10 40l2.5-8.3C10.9 29.5 8 25.7 8 20z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><ellipse cx="24" cy="20" rx="2" ry="2" fill="currentColor" opacity="0.5"/></svg>',
  // Infinity
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 28c-3 0-6-2.5-6-6s3-6 6-6c3 0 5 2 6 4s3 4 6 4 5-2 6-4 3-4 6-4c3 0 6 2.5 6 6s-3 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
  // Peace
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="24" r="18" stroke="currentColor" stroke-width="2"/><path d="M24 6v36M24 24l15 15M24 24L9 39" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
  // Brain with lightbulb idea
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M24 6C18 6 14 10 14 16c0 3.5 1.8 6.5 4.5 8.2V34h11V24.2C32.2 22.5 34 19.5 34 16c0-6-4-10-10-10z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M22 3h4v4h-4z" fill="currentColor" opacity="0.5"/><path d="M20 5l-3 5h14l-3-5" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" fill="none"/><circle cx="24" cy="10" r="3" fill="currentColor" opacity="0.3"/><path d="M24 13v3m-2 0h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M18 34h12v2H18z" fill="currentColor" opacity="0.3"/><path d="M19 38h10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M21 42h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
  // Head silhouette
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="24" cy="16" r="8" stroke="currentColor" stroke-width="2"/><path d="M12 44c0-6.6 5.4-12 12-12s12 5.4 12 12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
  // Heart pulse
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M24 40s-14-9-14-20c0-5.5 4-9 9-9 3 0 5 1.5 5 1.5s2-1.5 5-1.5c5 0 9 3.5 9 9 0 11-14 20-14 20z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M16 22h5l3 6 3-10 3 6h2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  // Lotus/calm
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M24 6C18 12 12 18 12 26c0 6 4 10 12 16 8-6 12-10 12-16 0-8-6-14-12-20z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M24 22c-3 3-6 8-6 12 0 2 2 4 6 7" stroke="currentColor" stroke-width="1" stroke-linejoin="round" opacity="0.5"/><path d="M24 22c3 3 6 8 6 12 0 2-2 4-6 7" stroke="currentColor" stroke-width="1" stroke-linejoin="round" opacity="0.5"/></svg>',
  // Sparkle/star
  '<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M24 4l4 12h13l-10 7 4 13-11-7-11 7 4-13-10-7h13z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>',
]

function randomBetween(a, b) {
  return a + Math.random() * (b - a)
}

export default {
  components: {
    ThemeToggle,
    LanguageSelector,
    DashboardCard,
    AssessmentModal,
    AssessmentGAD7,
    NLPChatModal,
  },
  setup() {
    const auth = useAuthStore();
    return { auth };
  },
  data() {
    return {
      modal: null,
      botSound: null,
      menuOpen: false,
      mouseX: 0.5,
      mouseY: 0.5,
      items: [],
    };
  },
  mounted() {
    this.botSound = new Audio('/sounds/bot-open.mp3');
    this.buildItems();
    this.animFrame = requestAnimationFrame(() => this.tick());
  },
  beforeUnmount() {
    if (this.animFrame) cancelAnimationFrame(this.animFrame);
  },
  methods: {
    buildItems() {
      const list = []
      for (let i = 0; i < 55; i++) {
        const svg = iconSvgs[i % iconSvgs.length]
        const size = randomBetween(20, 48)
        list.push({
          svg,
          refX: randomBetween(0, 100),
          refY: randomBetween(0, 100),
          x: 0, y: 0,
          vx: randomBetween(-0.3, 0.3),
          vy: randomBetween(-0.3, 0.3),
          radius: randomBetween(8, 25),
          speed: randomBetween(0.12, 0.35),
          size,
          opacity: randomBetween(0.06, 0.25),
          phase: randomBetween(0, Math.PI * 2),
        })
      }
      this.items = list
    },
    onMouseMove(e) {
      const rect = this.$refs.bgRef?.getBoundingClientRect()
      if (!rect) return
      this.mouseX = (e.clientX - rect.left) / rect.width
      this.mouseY = (e.clientY - rect.top) / rect.height
    },
    tick() {
      const bg = this.$refs.bgRef
      if (!bg) { this.animFrame = requestAnimationFrame(() => this.tick()); return }
      const rect = bg.getBoundingClientRect()
      const mxPx = this.mouseX * rect.width
      const myPx = this.mouseY * rect.height
      const now = Date.now() / 1000
      for (const item of this.items) {
        const angle = now * item.speed + item.phase
        const tx = Math.sin(angle) * item.radius
        const ty = Math.cos(angle * 0.7) * item.radius
        const px = item.refX + tx
        const py = item.refY + ty
        const ex = (px / 100) * rect.width
        const ey = (py / 100) * rect.height
        const dx = ex - mxPx
        const dy = ey - myPx
        const dist = Math.sqrt(dx * dx + dy * dy)
        const maxDist = 180
        const strength = Math.max(0, 1 - dist / maxDist)
        const repel = strength * strength * 80
        const a = Math.atan2(dy, dx)
        const rx = Math.cos(a) * repel
        const ry = Math.sin(a) * repel
        item.x = ex + rx
        item.y = ey + ry
      }
      const children = bg.children
      for (let i = 0; i < this.items.length; i++) {
        const el = children[i]
        if (!el) continue
        const item = this.items[i]
        el.style.left = (item.x - item.size / 2) + 'px'
        el.style.top = (item.y - item.size / 2) + 'px'
      }
      this.animFrame = requestAnimationFrame(() => this.tick())
    },
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
    handleLogout() {
      this.auth.logout();
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.floating-bg {
  position: fixed;
  width: 100%;
  height: 100%;
  z-index: 1;
  top: 0;
  left: 0;
  overflow: hidden;
}

.floating-inner svg {
  width: 100%;
  height: 100%;
  display: block;
  overflow: visible;
}

.floating-item {
  position: absolute;
  pointer-events: none;
  will-change: left, top;
}

.floating-inner svg {
  width: 100%;
  height: 100%;
  display: block;
  overflow: visible;
}

.background-glow {
  position: fixed;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, #5eead444, transparent 60%);
  animation: pulse 8s infinite;
  z-index: 0;
  pointer-events: none;
}

.container {
  padding: 1rem 2rem;
  max-width: 100%;
  min-height: 100vh;
  margin: auto;
  position: relative;
  z-index: 2;
}

.heading {
  text-align: center;
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--primary-teal);
  margin-bottom: 0.4rem;
  background: var(--bg-card-translucent);
  backdrop-filter: blur(6px);
  display: block;
  padding: 0.5rem 2rem;
  border-radius: 12px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
}
.sub {
  text-align: center;
  color: var(--text-muted);
  margin-bottom: 2rem;
  background: var(--bg-card-translucent);
  backdrop-filter: blur(6px);
  display: block;
  padding: 0.5rem 1.5rem;
  border-radius: 10px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
}

.navbar {
  background: var(--bg-card-translucent);
  backdrop-filter: blur(8px);
  color: var(--primary-teal);
  padding: 1rem 2rem;
  border-radius: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  box-shadow: 0 4px 16px var(--shadow-navbar);
  margin-bottom: 2rem;
  border-bottom: 2px solid var(--border-card);
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
  background-color: var(--bg-hover-teal);
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
  color: var(--text-footer);
  font-size: 0.85rem;
  background: var(--bg-card-translucent);
  backdrop-filter: blur(6px);
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
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
  background: var(--bg-card);
  color: var(--text-dark);
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

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.1); opacity: 1; }
}

@keyframes wave {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}
</style>
