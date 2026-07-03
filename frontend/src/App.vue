<template>
  <div id="app">
    <main class="app-wrapper">
      <router-view />
    </main>
  </div>
</template>

<script>
import { useThemeStore } from '@/stores/theme'
export default {
  name: "App",
  mounted() {
    useThemeStore().apply()
  }
}
</script>

<style>
body {
  margin: 0;
  background: var(--soft-gray);
}

#app {
  font-family: var(--font-family);
  color: var(--text-dark);
  min-height: 100vh;
}


</style>
