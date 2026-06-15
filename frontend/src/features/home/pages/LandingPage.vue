<template>
  <div class="landing-page">
    <div ref="vantaRef" class="vanta-background"></div>
    <div class="background-glow"></div>

    <div class="content-wrapper">
      <!-- MindCare SVG Logo -->
      <div class="logo-wrap">
        <svg width="72" height="72" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="36" cy="36" r="34" fill="#e6fff9" stroke="#0d9488" stroke-width="3"/>
          <path d="M22 30c0-7.7 6.3-14 14-14s14 6.3 14 14c0 5.2-2.8 9.7-7 12.2V52H29V42.2C24.8 39.7 22 35.2 22 30z" stroke="#0d9488" stroke-width="2.5" stroke-linejoin="round" fill="#f0fdfa"/>
          <path d="M29 52h14" stroke="#0d9488" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M31 56h10" stroke="#0d9488" stroke-width="2.5" stroke-linecap="round"/>
          <path d="M30 30c0-3.3 2.7-6 6-6" stroke="#5eead4" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>

      <h1 class="main-title">Welcome to <span>MindCare</span></h1>
      <p class="subtitle">Your mind matters. Talk safely, without judgement, at your own pace.</p>

      <div class="cards">
        <div class="card" @click="navigate('/mental-health')">
          <!-- Mental Health SVG icon -->
          <div class="card-icon-wrap">
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="32" cy="32" r="30" fill="#e6fff9"/>
              <path d="M32 16C24.3 16 18 22.3 18 30c0 5.2 2.8 9.7 7 12.2V48h14V42.2C43.2 39.7 46 35.2 46 30c0-7.7-6.3-14-14-14z" fill="#0d9488" opacity="0.15"/>
              <path d="M32 16C24.3 16 18 22.3 18 30c0 5.2 2.8 9.7 7 12.2V48h14V42.2C43.2 39.7 46 35.2 46 30c0-7.7-6.3-14-14-14z" stroke="#0d9488" stroke-width="2.5" stroke-linejoin="round"/>
              <path d="M25 48h14" stroke="#0d9488" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M27 52h10" stroke="#0d9488" stroke-width="2" stroke-linecap="round"/>
              <path d="M27 30c0-2.8 2.2-5 5-5" stroke="#5eead4" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h2>Mental Health</h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import * as THREE from 'three'

const vantaRef = ref(null)
let vantaEffect

onMounted(() => {
  const script = document.createElement('script')
  script.src = 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js'
  script.onload = () => {
    if (!vantaEffect && window.VANTA) {
      vantaEffect = window.VANTA.NET({
        el: vantaRef.value,
        THREE,
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.0,
        minWidth: 200.0,
        scale: 1.0,
        scaleMobile: 1.0,
        color: 0x0d9488,
        backgroundColor: 0xe6fff9,
        points: 10.0,
        maxDistance: 20.0,
        spacing: 15.0
      })
    }
  }
  document.body.appendChild(script)
})

onUnmounted(() => {
  if (vantaEffect) vantaEffect.destroy()
})

const router = useRouter()
function navigate(route) {
  router.push(route)
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(120deg, #e6fff9, #f0f9ff);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  font-family: 'Segoe UI', sans-serif;
}

.background-glow {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, #5eead444, transparent 60%);
  animation: pulse 8s infinite;
  z-index: 0;
}

.content-wrapper {
  position: relative;
  z-index: 1;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(8px);
  border-radius: 2rem;
  padding: 3rem;
  text-align: center;
  box-shadow: 0 8px 40px rgba(13, 148, 136, 0.18);
  max-width: 960px;
  width: 90%;
  color: #333;
  border: 1px solid rgba(94, 234, 212, 0.3);
}

.logo-wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 1.2rem;
}

.main-title {
  font-size: 2.8rem;
  margin-bottom: 0.5rem;
  font-weight: 800;
  color: #0f766e;
}

.main-title span {
  color: #0d9488;
}

.subtitle {
  font-size: 1.15rem;
  margin-bottom: 2.5rem;
  color: #444;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  justify-content: center;
}

.card {
  background: white;
  border-radius: 1.25rem;
  padding: 2rem 1.5rem;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(13, 148, 136, 0.12);
  transition: all 0.35s ease;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.card-icon-wrap {
  display: flex;
  justify-content: center;
}

.card h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0d9488;
  margin: 0;
}

.card:hover {
  background: linear-gradient(135deg, #0d9488, #0f766e);
  border-color: #5eead4;
  transform: translateY(-8px) scale(1.03);
  box-shadow: 0 16px 40px rgba(13, 148, 136, 0.35);
}

.card:hover h2 {
  color: white;
}

.card:hover .card-icon-wrap svg circle:first-child {
  fill: rgba(255,255,255,0.2);
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.1); opacity: 1; }
}

.vanta-background {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 0;
  top: 0;
  left: 0;
}
</style>
