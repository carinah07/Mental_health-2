<template>
  <div id="app">
    <main class="app-wrapper">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: "App"
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
