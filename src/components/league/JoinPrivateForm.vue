<template>
  <form ref="form" @submit.prevent="submit" class="form-inline">
    <div class="form-group">
      <label class="sr-only">League ID</label>
      <input type="text" v-model="leagueId" class="form-control" placeholder="League ID" required />
    </div>

    <div class="form-group">
      <label class="sr-only">Password</label>
      <input
        type="text"
        v-model="leaguePassword"
        class="form-control"
        placeholder="Password"
        required
      />
    </div>

    <button type="submit" class="btn btn-default">Join</button>
  </form>
</template>

<script>
export default {
  name: "join-private-form",
  props: {
    leagueId: String,
    leaguePassword: String,
  },
  data() {
    return {
      league: null,
    }
  },
  methods: {
    submit() {},
    joinLeague() {},
  },
  computed: {
    uid() {
      return this.$store.state.uid
    },
  },
}
</script>