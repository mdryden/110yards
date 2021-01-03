<template>
  <div class="mdc-touch-target-wrapper">
    <button class="mdc-button mdc-button--touch mdc-button--raised">
      <div class="mdc-button__ripple"></div>
      <span class="mdc-button__label"><slot /></span>
      <div class="mdc-button__touch"></div>
    </button>
  </div>
</template>

<style scoped>
button.mdc-button--raised {
  color: var(--text-color);
  background-color: var(--color-primary);
  border-color: var(--color-secondary);
}

button a {
  text-decoration: none;
}
</style>

<script>
export default {
  components: {},
  props: {
    classes: Array,
  },
}
</script>
