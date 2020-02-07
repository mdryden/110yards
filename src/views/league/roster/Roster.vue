<template>
  <table class="table table-condensed">
    <thead>
      <tr>
        <th colspan="2">{{ roster.name }}</th>
        <th :colspan="includeProjection ? 2 : 1" class="text-right">
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
    <roster-row :includeProjection="includeProjection" v-for="spot in activeRosterSpots" :key="spot.id">
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
    <roster-row :includeProjection="includeProjection" v-for="spot in benchPlayers" :key="spot.id" />
    <tr>
      <th>Bench</th>
      <th></th>
      <th></th>
      <th class="text-right">{{ benchScore }}</th>
      <th v-if="includeProjection" class="text-right">{{ benchProjection }}</th>
      }
    </tr>
  </table>
</template>

<script>
import RosterRow from "./RosterRow.vue"

export default {
  name: "roster",
  components: {
    RosterRow,
  },
  props: {
    roster: Object,
    isCurrentWeek: Boolean,
  },
  computed: {
    currentLeague() {
      return this.$store.state.currentLeague
    },
    includeProjection() {
      return this.isCurrentWeek
    },
    activeRosterSpotsCount() {
      return this.currentLeague.active_roster_spots // todo: store this when configuring rosters
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
    benchPlayers() {
      return [] // todo: implement
    },
    benchScore() {
        return 0;
    },
    benchProjection() {
        return 0;
    }
  },
}
</script>
