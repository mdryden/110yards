<template>
  <div id="app">
    <nav-bar />
    <div class="container" id="body" :data-version="version">
      <router-view />
      <throbber />
      <div id="footer">
        <p>&copy; 2020 Michael Dryden</p>
        <p :title="'Version ' + version">Last release {{ lastUpdated }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
#footer {
  padding-top: 2em;
  margin: auto;
  width: 50%;
  text-align: center;
  font-size: small;
  color: gray;
}
</style>

<script>
import NavBar from "./components/NavBar"
import Throbber from "./components/Throbber"
import moment from "moment"

export default {
  name: "app",
  components: {
    NavBar,
    Throbber,
  },
  computed: {
    version() {
      return process.env.VUE_APP_VERSION || "0000000"
    },
    lastUpdated() {
      return moment(this.getLastUpdated()).fromNow()
    },
  },
  methods: {
    getLastUpdated() {
      return "2020-01-21T04:28+00:00" || new Date()
      //return process.env.VUE_APP_LAST_UPDATED || new Date()
    },
  },
}
</script>
