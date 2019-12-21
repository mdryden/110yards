<template>
  <div class="row">
    <div class="col-md-6">
      <form ref="form" @submit.prevent="submit">
        <h4>Create a fantasy league</h4>
        <hr />

        <div class="form-group">
          <!-- <label>League Name</label> -->
          <input
            type="text"
            v-model="leagueName"
            placeholder="League Name"
            class="form-control"
            required
          />
        </div>

        <div class="form-group">
          <label class="control-label">Make this league private?</label>
          <div class="form-check">
            <label class="checkbox-inline">
              <input type="checkbox" v-model="isPrivate" class="form-check-input" />Yes
              <small>(Private leagues are hidden from the listing, and require a password to join)</small>
            </label>
          </div>
        </div>

        <div class="form-group" id="passwordGroup" v-show="isPrivate">
          <label class="control-label">League Password</label>
          <input type="text" v-model="password" class="form-control" />
        </div>

        <button type="submit" class="btn btn-primary">Create</button>
      </form>
    </div>
  </div>
</template>

<script>
import * as leagueService from "../../api/110yards/league"

export default {
  name: "create-league",
  components: {},
  data() {
    return {
      leagueName: null,
      isPrivate: false,
      password: null,
    }
  },
  methods: {
    submit() {
      if (this.$refs.form.checkValidity()) {
        this.create()
      } else {
        this.$refs.form.reportValidity()
      }
    },
    async create() {
      let user = this.$store.state.currentUser

      if (user == null) {
        alert("You are not logged in")
        this.submitting = false
        return
      }

      try {
        let league = {
          name: this.leagueName,
          private: this.isPrivate,
          password: this.password,
        }

        league = await leagueService.create(user, league)

        this.$router.push({ name: "league", params: { leagueId: league.id } })
      } catch (exception) {
        console.error(exception.message)
        alert("Unable to create league")
      }
    },
  },
}
</script>