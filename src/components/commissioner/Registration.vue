<template>
  <div class="row">
    <div class="col-md-6 registration-control">
      <!-- todo: apply rules - can't change if league is locked -->
      <div v-if="league.registration_closed">
        <p>
          Registration for this league has been closed, so no other managers may
          join.
        </p>
        <button class="btn btn-default" v-on:click="reopenRegistration()">
          Re-open registrations
        </button>
      </div>
      <div v-if="!league.is_full && !league.registration_closed">
        <p>
          Registration for this league is open. To prevent new registrations,
          generate a schedule or click here:
        </p>
        <button class="btn btn-default" v-on:click="closeRegistration()">
          Close registrations
        </button>
      </div>
    </div>
    <div class="col-md-6 invite-options">
      <h6>Invite managers by email:</h6>
      <div class="form-inline">
        <div class="form-group">
          <input
            type="text"
            ref="invite-email"
            class="form-control"
            placeholder="Recipient email"
          />
          <button class="btn btn-primary" v-on:click="sendInvite()">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
      <h6>Or send this link:</h6>
      <div class="form-inline">
        <div class="form-group">
          <input
            type="text"
            class="form-control"
            v-model="joinLink"
            id="join-link"
          />
          <button class="btn btn-primary" v-on:click="copyJoinLink()">
            <i class="fas fa-copy"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import router from "../../modules/router"
import * as leagueService from "../../api/110yards/league"
import { firestore } from "../../modules/firebase"

export default {
  name: "registration",
  props: {
    league: Object,
  },
  data() {
    return {
      privateConfig: null,
      joinLink: null,
    }
  },
  computed: {
    password() {
      return this.privateConfig ? this.privateConfig.password : null
    },

    user() {
      return this.$store.state.currentUser
    },
  },
  methods: {
    copyJoinLink() {
      let element = document.getElementById("join-link")
      element.select()
      document.execCommand("copy")
    },
    setJoinLink() {
      let params = { joinId: this.league.id }
      let query = {}

      if (this.password != null) {
        query = { password: this.privateConfig.password }
      }

      let route = router.resolve({
        name: "join-direct",
        params: params,
        query: query,
      })
      this.joinLink = `${window.location.origin}${route.href}`
    },
    async reopenRegistration() {
      await leagueService.openRegistration(this.user, this.league.id)
    },
    async closeRegistration() {
      await leagueService.closeRegistration(this.user, this.league.id)
    },
  },
  watch: {
    league: {
      immediate: true,
      handler(league) {
        if (league == null) return
        let ref = firestore
          .collection("league")
          .doc(league.id)
          .collection("config")
          .doc("private")
        this.$bind("privateConfig", ref)
      },
    },
    password: {
      immediate: true,
      handler(password) {
        this.setJoinLink()
      },
    },
  },
}
</script>

<style scoped>
.registration-control {
  padding-bottom: 2em;
}
</style>
