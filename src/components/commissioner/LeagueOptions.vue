<template>
  <div class="row">
    <div class="col-md-6">
      <form ref="form" @submit.prevent="submit()">
        <div class="form-group">
          <label>League Name</label>
          <input
            type="text"
            v-model="form.name"
            placeholder="League Name"
            class="form-control"
            required
          />
        </div>

        <div class="form-group">
          <label class="control-label">Make this league private?</label>
          <div class="form-check">
            <label class="checkbox-inline">
              <input
                type="checkbox"
                v-model="form.isPrivate"
                class="form-check-input"
              />Yes
              <small
                >(Private leagues are hidden from the listing, and require a
                password to join)</small
              >
            </label>
          </div>
        </div>

        <div class="form-group" id="passwordGroup" v-show="form.isPrivate">
          <label class="control-label">League Password</label>
          <input type="text" v-model="form.password" class="form-control" />
        </div>

        <button type="submit" class="btn btn-default">Update</button>
        <saved-indicator :saved="saved" />
      </form>
    </div>
  </div>
</template>

<script>
import { firestore } from "../../modules/firebase"
import * as leagueService from "../../api/110yards/league"
import SavedIndicator from "../SavedIndicator"

export default {
  name: "league-options",
  components: {
    SavedIndicator,
  },
  props: {
    league: Object,
  },
  data() {
    return {
      form: {
        name: null,
        isPrivate: false,
        password: null,
      },
      saved: false,
    }
  },
  methods: {
    submit() {
      if (this.$refs.form.checkValidity()) {
        this.save()
      } else {
        this.$refs.form.reportValidity()
      }
    },
    async save() {
      let user = this.$store.state.currentUser
      let updatedLeague = {
        id: this.league.id,
        name: this.form.name,
        private: this.form.isPrivate,
        password: this.form.password,
      }
      await leagueService.update(user, updatedLeague)
      this.saved = true
    },
  },
  watch: {
    league: {
      immediate: true,
      async handler(league) {
        if (league == null) return

        let privateSettings = (
          await firestore
            .collection("league")
            .doc(league.id)
            .collection("config")
            .doc("private")
            .get()
        ).data()

        this.form.name = league.name
        this.form.isPrivate = league.private
        this.form.password = privateSettings.password
      },
    },
    form: {
      deep: true,
      handler(form) {
        this.saved = false
      },
    },
  },
}
</script>
