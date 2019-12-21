<template>
  <div id="app">
    <nav-bar />
    <div class="container" id="body">
      <router-view />
      <throbber />
    </div>
  </div>
</template>

<script>
import NavBar from "./components/NavBar"
import Throbber from "./components/Throbber"

export default {
  name: "app",
  components: {
    NavBar,
    Throbber,
  },
}
</script>
