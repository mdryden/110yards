<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <router-link to="/" class="navbar-item">
        <img
          class="logo-small"
          src="/assets/img/football-white.png"
          alt="110 yards"
        />
        <label class="is-sr-only">Home</label>
      </router-link>

      <a
        role="button"
        class="navbar-burger"
        aria-label="menu"
        aria-expanded="false"
        data-target="site-navbar"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div id="site-navbar" class="navbar-menu">
      <router-link
        v-if="leagueId"
        class="navbar-item"
        :to="{ name: 'league', params: { leagueId: leagueId } }"
      >
        League
      </router-link>

      <router-link
        v-if="leagueId && userId"
        class="navbar-item"
        :to="{
          name: 'roster',
          params: { leagueId: leagueId, rosterId: userId },
        }"
      >
        My Team
      </router-link>

      <router-link
        v-if="leagueId"
        class="navbar-item"
        :to="{ name: 'league-players', params: { leagueId: leagueId } }"
      >
        Players
      </router-link>

      <router-link class="navbar-item" to="/faq">FAQ</router-link>

      <router-link v-if="isAdmin" class="navbar-item" to="/admin">
        Admin
      </router-link>
      <router-link
        id="login"
        v-if="isAnonymous"
        class="navbar-item"
        to="/login"
      >
        Log in
      </router-link>
      <!-- <span class="nav-item navbar-text">{{username}}</span> -->
      <a
        id="logout"
        v-if="!isAnonymous"
        class="navbar-item"
        href="#"
        @click="logOut"
      >
        Log out
      </a>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background-color: var(--color-primary);
  background-image: none;
}

.navbar img.logo-small {
  height: 40px;
}

.navbar-brand {
  margin-top: -8px;
}

a.navbar-item:hover {
  color: white;
  background-color: inherit;
}
</style>

<script>
import { auth } from "../modules/firebase"

// TODO: navbar needs to close when I click a link
export default {
  name: "nav-bar",
  data() {
    return {
      visible: false,
      rosterId: null,
    }
  },
  computed: {
    isAnonymous() {
      return this.$store.state.isAnonymous
    },
    username() {
      return this.isAnonymous ? "" : this.$store.state.currentUser.displayName
    },
    userId() {
      return this.isAnonymous ? "" : this.$store.state.uid
    },
    leagueId() {
      return this.$store.state.currentLeagueId
    },
    isAdmin() {
      return this.$store.state.isAdmin
    },
  },
  methods: {
    async logOut() {
      await auth.signOut()
      this.$router.replace("/")
    },
  },
}
</script>
