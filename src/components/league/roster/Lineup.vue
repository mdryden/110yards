<template>
  <table v-if="rostersConfig" class="table table-condensed">
    <thead>
      <tr>
        <th :colspan="includeProjection ? 5 : 4" class="text-right">
          {{ playedCount }} / {{ activeRosterSpotsCount }} played
        </th>
      </tr>
      <tr>
        <th>Pos</th>
        <th>Name</th>
        <th>Opp</th>
        <th class="text-right">Pts</th>
        <th class="text-right" v-if="includeProjection">Proj</th>
      </tr>
    </thead>
    <lineup-spot
      :includeProjection="includeProjection"
      v-for="spot in activeRosterSpots()"
      :key="spot.id"
      :spot="spot"
      :player="getPlayerInSpot(spot)"
    />
    <tr>
      <th>Total</th>
      <th></th>
      <th></th>
      <th class="text-right">{{ totalScore }}</th>
      <th v-if="includeProjection" class="text-right">{{ totalProjection }}</th>
    </tr>
    <tr>
      <td :colspan="includeProjection ? 5 : 4">&nbsp;</td>
    </tr>
    <lineup-spot
      :includeProjection="includeProjection"
      v-for="spot in benchSpots()"
      :key="spot.id"
      :spot="spot"
      :player="getPlayerInSpot(spot)"
    />
    <lineup-spot
      :includeProjection="includeProjection"
      v-for="spot in reserveRosterSpots()"
      :key="spot.id"
      :spot="spot"
      :player="getPlayerInSpot(spot)"
    />
    <tr>
      <th>Bench</th>
      <th></th>
      <th></th>
      <th class="text-right">{{ benchScore }}</th>
      <th v-if="includeProjection" class="text-right">{{ benchProjection }}</th>
    </tr>
  </table>
</template>

<script>
import { firestore } from "../../../modules/firebase"
import LineupSpot from "./LineupSpot.vue"

export default {
  name: "lineup",
  components: {
    LineupSpot,
  },
  props: {
    roster: Object,
    leagueId: String,
    includeProjection: Boolean,
  },
  data() {
    return {
      rostersConfig: null,
      league: null,
    }
  },
  computed: {
    activeRosterSpotsCount() {
      return this.rostersConfig.active_roster_spots // todo: store this when configuring rosters
    },
    playedCount() {
      return 0 //todo: implement
    },
    activePlayers() {
      return [] // todo: implement
    },
    totalScore() {
      return 0 // todo: implement
    },
    totalProjection() {
      return 0 // todo: implement
    },
    benchScore() {
      return 0
    },
    benchProjection() {
      return 0
    },
  },
  methods: {
    activeRosterSpots() {
      if (!this.rostersConfig) return null

      return this.rostersConfig.roster.filter(
        spot => !spot.reserve && spot.type != "bench",
      )
    },
    benchSpots() {
      // todo: this needs to create bench spots for players who are not in a defined bench spot
      return this.rostersConfig.roster.filter(spot => spot.type == "bench")
    },
    reserveRosterSpots() {
      if (!this.rostersConfig) return null

      return this.rostersConfig.roster.filter(spot => spot.reserve)
    },
    getPlayerInSpot(spot) {
      return null
    },
  },
  watch: {
    leagueId: {
      immediate: true,
      handler(leagueId) {
        if (!leagueId) return

        let leagueRef = firestore.collection("league").doc(leagueId)

        let rostersRef = leagueRef.collection("config").doc("rosters")

        this.$bind("league", leagueRef)
        this.$bind("rostersConfig", rostersRef)
      },
    },
  },
}
</script>
