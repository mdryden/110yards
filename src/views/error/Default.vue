<template>
  <div>
    <h1>Oh no.</h1>
    <h2>Something went wrong. Sorry about that.</h2>
    <p>
      The error has been logged, but you may also want to
      <a href="https://github.com/mdryden/110yards/issues" target="_blank"
        >contact the admin</a
      >, and let him know what happened.
    </p>
    <pre class="error">&gt; {{ message }}</pre>
  </div>
</template>

<style scoped>
.error {
  color: red;
}
</style>

<script>
//todo: log the error somehow.  stack driver? (abstraction)
export default {
  computed: {
    message() {
      return this.$route.params.message
    },
  },
}
</script>
