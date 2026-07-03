import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

export function useVantaBackground() {
  const vantaRef = ref(null)
  let vantaEffect

  function initVanta() {
    if (!vantaRef.value || vantaEffect || !window.VANTA?.NET) return

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
      spacing: 15.0,
    })
  }

  onMounted(() => {
    window.THREE = THREE

    if (window.VANTA?.NET) {
      initVanta()
      return
    }

    const script = document.createElement('script')
    script.src = 'https://cdn.jsdelivr.net/npm/vanta@0.5.24/dist/vanta.net.min.js'
    script.onload = initVanta
    script.onerror = () => console.error('Failed to load Vanta background effect')
    document.head.appendChild(script)
  })

  onUnmounted(() => {
    if (vantaEffect) {
      vantaEffect.destroy()
      vantaEffect = null
    }
  })

  return { vantaRef }
}
