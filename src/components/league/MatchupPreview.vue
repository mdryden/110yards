<template>
  <tr class="matchup" v-on:click="viewMatchup()">
    <td class="roster roster-away">
      <div v-if="matchup.away" class="team-name">
        <router-link
          :to="{
            name: 'roster',
            params: { leagueId: leagueId, rosterId: matchup.away.uid },
          }"
          >{{ matchup.away.name }}</router-link
        >
        <div class="record">{{ matchup.away.record }}</div>
      </div>
      <div v-if="!matchup.away" class="team-name">{{ noTeamText }}</div>
    </td>
    <td
      class="score score-away"
      :class="matchupStateClass(matchup.away_score, matchup.home_score)"
    >
      {{ matchup.away_score }}
      <!-- todo: format decimals -->
    </td>

    <td
      class="score score-home"
      :class="matchupStateClass(matchup.home_score, matchup.away_score)"
    >
      {{ matchup.home_score }}
    </td>
    <td class="roster roster-home">
      <div v-if="matchup.home" class="team-name">
        <router-link
          :to="{
            name: 'roster',
            params: { leagueId: leagueId, rosterId: matchup.home.uid },
          }"
          >{{ matchup.home.name }}</router-link
        >
        <div class="record">{{ matchup.home.record }}</div>
      </div>
      <p v-if="!matchup.home" class="team-name">TBD</p>
    </td>
  </tr>
</template>

<style scoped>
.team-name {
  text-align: center;
}
</style>

<script>
export default {
  name: "matchup-preview",
  props: {
    matchup: Object,
    leagueId: String,
  },
  computed: {
    noTeamText() {
      return this.leagueStarted ? "Bye" : "TBD"
    },
  },
  methods: {
    matchupStateClass(scoreFor, scoreAgainst) {
      return scoreFor > scoreAgainst ? "winning" : ""
    },
    viewMatchup() {
      this.$router.push({
        name: "matchup",
        params: { leagueId, matchupId: matchup.id },
      })
    },
  },
}
</script>
