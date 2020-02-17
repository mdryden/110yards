<template>
  <form ref="form" @submit.prevent="trySignup()" class="form-inline">
    <div class="form-group">
      <label class="sr-only">League ID</label>
      <input
        type="text"
        v-model="leagueId"
        class="form-control"
        placeholder="League ID"
        required
      />
    </div>

    <div class="form-group">
      <label class="sr-only">Password</label>
      <input
        type="text"
        v-model="password"
        class="form-control"
        placeholder="Password"
      />
    </div>

    <button type="submit" class="btn btn-default">Join</button>
  </form>
</template>

<script>
import eventBus from "../../modules/eventBus"
import * as leagueService from "../../api/110yards/league"

export default {
  name: "join-private-form",
  data() {
    return {
      joining: false,
      failed: false,
      leagueId: null,
      password: null,
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.currentUser
    },
  },
  methods: {
    async trySignup() {
      if (this.leagueId && this.currentUser) {
        this.joining = true

        let result = await leagueService.join(
          this.currentUser,
          this.leagueId,
          this.password,
        )

        if (result.success) {
          this.$router.push({
            name: "league",
            params: { leagueId: this.leagueId },
          })
        } else {
          alert(result.message)
        }
      }
    },
  },
  watch: {
    joinId: {
      immediate: true,
      async handler(joinId) {
        this.leagueId = joinId
      },
    },
    currentUser: {
      immediate: true,
      async handler(currentUser) {
        //await this.trySignup()
      },
    },
  },
  mounted: function() {
    this.password = this.$route.query.password
    this.leagueId = this.$route.params.joinId
  },
}
</script>
