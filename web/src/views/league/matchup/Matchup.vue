<template>
  <v-sheet v-if="league && matchup">
    <matchup-header
      :matchup="matchup"
      :away="awayRoster"
      :home="homeRoster"
      :weekNumber="weekNumber"
      :enableProjections="enableProjections"
      :isCurrentWeek="isCurrentWeek"
    />

    <matchup-vs
      class="d-none d-md-block"
      :league="league"
      :away="awayRoster"
      :home="homeRoster"
      :enableProjections="enableProjections"
      :weekNumber="weekNumber"
    />
    <matchup-vs
      class="d-md-none"
      mobile
      :league="league"
      :away="awayRoster"
      :home="homeRoster"
      :enableProjections="enableProjections"
      :weekNumber="weekNumber"
    />
  </v-sheet>
</template>

<style scoped>
.heading {
  border-bottom: 1px solid black;
}

.active {
  font-weight: bold;
}
</style>

<script>
import { firestore } from "../../../modules/firebase"
import { matchupType } from "../../../api/110yards/constants"
import MatchupVs from "../../../components/league/matchup/MatchupVs.vue"
import scoreboard from "../../../mixins/scoreboard"
import MatchupHeader from "../../../components/league/matchup/MatchupHeader.vue"

export default {
  name: "matchup",
  components: {
    MatchupVs,
    MatchupHeader,
  },
  mixins: [scoreboard],
  props: {
    leagueId: {
      type: String,
      required: true,
    },
    weekNumber: {
      required: true,
    },
    matchupId: {
      required: true,
    },
  },
  data() {
    return {
      matchup: null,
      awayRoster: null,
      homeRoster: null,
      league: null,
    }
  },
  computed: {
    enableProjections() {
      return this.isCurrentWeek && this.$root.enableProjections
    },

    isCurrentWeek() {
      return this.weekNumber == this.$root.state.current_week
    },

    title() {
      if (!this.matchup) return null

      return this.matchup.type == matchupType.Regular ? `Week ${this.weekNumber}` : this.matchup.type_display
    },

    includeProjection() {
      return true
    },
  },
  methods: {
    configureLeagueReference() {
      if (!this.leagueId) return

      let ref = firestore.collection("league").doc(this.leagueId)
      this.$bind("league", ref)
    },

    configureMatchupReference() {
      if (!this.leagueId || !this.weekNumber || !this.matchupId) return

      let path = `league/${this.leagueId}/week/${this.weekNumber}/matchup/${this.matchupId}`
      let ref = firestore.doc(path)

      this.$bind("matchup", ref)
    },

    configureRosterReferences() {
      if (!this.matchup || !this.matchup.away || !this.matchup.home) return

      let leagueRef = firestore.doc(`league/${this.leagueId}`)
      this.$bind("league", leagueRef)

      if (this.isCurrentWeek) {
        let rostersRef = firestore.collection(`league/${this.leagueId}/roster`)
        let awayRef = rostersRef.doc(this.matchup.away.id)
        let homeRef = rostersRef.doc(this.matchup.home.id)

        this.$bind("awayRoster", awayRef)
        this.$bind("homeRoster", homeRef)
      } else {
        this.awayRoster = this.matchup.away
        this.homeRoster = this.matchup.home
      }
    },
  },
  watch: {
    matchupId: {
      immediate: true,
      handler(matchupId) {
        this.configureMatchupReference()
      },
    },
    leagueId: {
      immediate: true,
      handler(leagueId) {
        this.configureLeagueReference()
        this.configureMatchupReference()
      },
    },
    weekNumber: {
      immediate: true,
      handler(weekNumber) {
        this.configureMatchupReference()
      },
    },
    matchup: {
      handler(matchup) {
        this.configureRosterReferences()
      },
    },
  },
}
</script>
