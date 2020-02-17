<template>
  <tr class="matchup">
    <td class="roster roster-away">
      <div v-if="matchup.away">
        <router-link
          :to="{
            name: 'roster',
            params: { leagueId: leagueId, rosterId: matchup.away.uid },
          }"
          >{{ matchup.away.name }}</router-link
        >
        <div class="record">{{ matchup.away.record }}</div>
      </div>
      <div v-if="!matchup.away">{{ noTeamText }}</div>
    </td>
    <td
      class="score score-away"
      :class="matchupStateClass(matchup.away_score, matchup.home_score)"
    >
      {{ formatScore(matchup.away_score) }}
    </td>
    <td class="vs">
      <router-link
        :to="{
          name: 'matchup',
          params: {
            leagueId: leagueId,
            weekNumber: weekNumber,
            matchupId: matchup.id,
          },
        }"
        >vs</router-link
      >
    </td>
    <td
      class="score score-home"
      :class="matchupStateClass(matchup.home_score, matchup.away_score)"
    >
      {{ formatScore(matchup.home_score) }}
    </td>
    <td class="roster roster-home">
      <div v-if="matchup.home">
        <router-link
          :to="{
            name: 'roster',
            params: { leagueId: leagueId, rosterId: matchup.home.uid },
          }"
          >{{ matchup.home.name }}</router-link
        >
        <div class="record">{{ matchup.home.record }}</div>
      </div>
      <p v-if="!matchup.home">TBD</p>
    </td>
  </tr>
</template>

<style scoped>
.matchup td.roster {
  width: 35%;
}

.matchup td.score {
  width: 15%;
}

.matchup td {
  border-top: 1px solid var(--bg-color-secondary);
}
.roster-away {
  text-align: left;
}
.score-away {
  text-align: right;
  vertical-align: middle;
  padding-right: 1em;
  border-right: 1px solid var(--bg-color-secondary);
}
.roster-home {
  text-align: right;
}
.score-home {
  padding-left: 1em;
  vertical-align: middle;
  border-left: 1px solid var(--bg-color-secondary);
}
.record {
  font-size: small;
}
td.vs {
  vertical-align: middle;
  padding-left: 1em;
  padding-right: 1em;
}
</style>

<script>
import * as formatter from "../../modules/formatter"

export default {
  name: "matchup-preview",
  props: {
    matchup: Object,
    leagueId: String,
    weekNumber: Number,
  },
  computed: {
    noTeamText() {
      return this.leagueStarted ? "Bye" : "TBD"
    },
  },
  methods: {
    formatScore(score) {
      return formatter.formatScore(score)
    },
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
