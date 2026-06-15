<template>
  <div class="card" @click="$emit('click')">
    <div class="icon">
      <slot name="icon" />
    </div>
    <div class="label">{{ title }}</div>
    <p>{{ description }}</p>
  </div>
</template>

<script>
export default {
  props: ["title", "description"]
}
</script>

<style scoped>
.card {
  background: linear-gradient(135deg, #f0fdfa 0%, #e6fff9 100%);
  border-left: 6px solid var(--primary-teal);
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
  box-shadow: 0 4px 14px rgba(13, 148, 136, 0.1);
}
.card:hover {
  transform: translateY(-6px);
  background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
  box-shadow: 0 10px 24px rgba(13, 148, 136, 0.3);
}
.card:hover .label,
.card:hover p {
  color: white;
}
.card:hover .icon svg {
  stroke: white;
  fill: none;
}
.card:hover .icon svg circle,
.card:hover .icon svg path,
.card:hover .icon svg rect,
.card:hover .icon svg line,
.card:hover .icon svg polyline {
  stroke: white;
}
.icon {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
}
.label {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--primary-teal);
  margin-bottom: 6px;
}
p {
  font-size: 0.88rem;
  color: #555;
  margin: 0;
}
</style>
