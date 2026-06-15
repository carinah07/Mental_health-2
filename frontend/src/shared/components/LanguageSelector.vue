<template>
  <div class="lang-switch">
    <label>{{ $t("language") }}:</label>
    <select v-model="locale" @change="switchLang">
      <option value="en">English</option>
      <option value="sw">Kiswahili</option>
    </select>
  </div>
</template>

<script>
export default {
  data() {
    return { locale: this.$i18n.locale }
  },
  methods: {
    switchLang() {
      this.$i18n.locale = this.locale
    }
  }
}
</script>

<style scoped>
.lang-switch {
  background: var(--primary-teal);
  padding: 8px 12px;
  border-radius: 10px;
  color: var(--text-light);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}
select {
  margin-left: 10px;
  padding: 4px 8px;
  border-radius: 6px;
  border: none;
  font-size: 0.85rem;
}
</style>
