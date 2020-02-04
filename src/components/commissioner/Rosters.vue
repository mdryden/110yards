<template>
  <div class="row">
    <p class="info">
      Quarterback, running back and kicker slots are capped at 1 maximum, for
      gameplay reasons.
    </p>
    <div class="col-sm-12">
      <form ref="form" @submit.prevent="submit()">
        <table class="table">
          <thead>
            <tr>
              <th>Position</th>
              <th>Count</th>
              <th></th>
            </tr>
          </thead>
          <tr v-for="position in rosterPositions" :key="position.id">
            <th class="position">{{ position.display }}</th>
            <td class="count">
              <input
                type="number"
                class="form-control"
                v-model.number="leaguePositions[position.id]"
                :data-position-id="position.id"
                required
                :max="position.max"
              />
            </td>
            <td class="description">{{ position.description }}</td>
          </tr>

          <!-- todo: non-starting spots -->
        </table>

        <button class="btn btn-default">Save changes</button>
        <saved-indicator :saved="saved" />
      </form>
    </div>
  </div>
</template>

<style scoped>
.table td {
  padding-bottom: 0.5em;
}
.position {
  width: 25%;
}

.count {
  min-width: 4em;
  width: 10%;
}

.description {
  padding-left: 1em;
  font-size: small;
}
</style>

<script>
import { firestore } from "../../modules/firebase"
import * as leagueService from "../../api/110yards/league"
import SavedIndicator from "../SavedIndicator"

export default {
  name: "rosters",
  components: {
    SavedIndicator,
  },
  props: {
    leagueId: String,
  },
  data() {
    return {
      leaguePositions: {},
      rosterPositions: [],
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
      await leagueService.updateRosterPositions(
        user,
        this.leagueId,
        this.leaguePositions,
      )

      this.saved = true
    },

    async bindLeague(leagueId) {
      let league = (
        await firestore
          .collection("league")
          .doc(leagueId)
          .get()
      ).data()
      this.leaguePositions = league.positions
    },

    async bindPositions() {
      await this.$bind(
        "rosterPositions",
        firestore.collection("roster-positions").orderBy("order"),
      )
    },
  },
  watch: {
    leagueId: {
      immediate: true,
      async handler(leagueId) {
        if (leagueId == null) return

        try {
          let promises = []
          promises.push(this.bindLeague(leagueId))
          promises.push(this.bindPositions())

          await Promise.all(promises)
        } catch (exception) {
          this.$eventBus.$emit("exception", exception)
        }
      },
    },
    leaguePositions: {
      deep: true,
      handler(leaguePositions) {
        this.saved = false
      },
    },
  },
}
</script>
