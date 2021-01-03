<template>
  <div class="mdc-touch-target-wrapper">
    <router-link
      :to="{ name: 'join-league' }"
      class="mdc-button mdc-button--touch mdc-button--raised"
      >Join a league</router-link
    >
    <div class="mdc-button__touch"></div>
  </div>
</template>

<style scoped>
a.mdc-button--raised {
  color: var(--text-color);
  background-color: var(--color-primary);
  border-color: var(--color-secondary);
}

a:hover {
  text-decoration: underline;
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
