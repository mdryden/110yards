<template>
  <tr class="matchup" v-on:click="viewMatchup()">
    <td class="roster roster-away">
      <p v-if="matchup.away">
        <router-link
          :to="{
            name: 'roster',
            props: { leagueId, rosterId: matchup.away.id },
          }"
          >{{ matchup.away.name }}</router-link
        >
        <small>{{ matchup.away.record }}</small>
      </p>
      <p v-if="!matchup.away">{{ noTeamText }}</p>
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
      <p v-if="matchup.home">
        <router-link
          :to="{
            name: 'roster',
            props: { leagueId, rosterId: matchup.home.id },
          }"
          >{{ matchup.home.name }}</router-link
        >
        <small>{{ matchup.home.record }}</small>
      </p>
      <p v-if="!matchup.home">TBD</p>
    </td>
  </tr>
</template>

<script>
export default {
  name: "matchup-preview",
  props: {
    matchup: Object,
    leagueId: String,
    leagueStarted: Boolean,
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
