<template>
  <div class="row" v-if="week">
    <div class="col-md-12">
      <h4>{{ title }}</h4>
      <hr />
      <div class="row">
        <div class="col-md-6">
          <h5>{{ matchup.away.name }}</h5>
          <lineup
            :roster="matchup.away"
            :includeProjection="includeProjection"
            :leagueId="leagueId"
          />
        </div>
        <div class="col-md-6">
          <h5>{{ matchup.home.name }}</h5>
          <lineup
            :roster="matchup.home"
            :includeProjection="includeProjection"
            :leagueId="leagueId"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { firestore } from "../../../modules/firebase"
import Lineup from "../../../components/league/roster/Lineup"

export default {
  name: "matchup",
  components: {
    Lineup,
  },
  props: {
    leagueId: String,
    weekNumber: String,
    matchupId: String,
  },
  data() {
    return {
      bound: false,
      week: null,
    }
  },
  computed: {
    matchup() {
      if (!this.matchupId || !this.week) return null

      return this.week.matchups[this.matchupId - 1]
    },
    title() {
      if (!this.week) return null

      return `${this.week.heading}: ${this.matchup.away.name} vs ${this.matchup.home.name}`
    },

    includeProjection() {
      return true
    },
  },
  methods: {
    bindMatchups() {
      if (this.bound) return
      if (!this.leagueId || !this.weekNumber) return

      let paddedWeekNumber = this.weekNumber.padStart(2, "0")

      let ref = firestore
        .collection("league")
        .doc(this.leagueId)
        .collection("weeks")
        .doc(paddedWeekNumber)
      this.$bind("week", ref)
    },
  },
  watch: {
    matchupId: {
      immediate: true,
      handler(matchupId) {
        this.bindMatchups()
      },
    },
    leagueId: {
      immediate: true,
      handler(leagueId) {
        this.bindMatchups()
      },
    },
    weekNumber: {
      immediate: true,
      handler(weekNumber) {
        this.bindMatchups()
      },
    },
  },
}
</script>
