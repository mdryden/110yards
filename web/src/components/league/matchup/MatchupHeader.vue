<template>
  <v-row v-if="leagueId && weekNumber" class="heading mb-2 text-right">
    <v-col cols="5" class="roster-name pl-4">
      <v-row>
        <v-col class="pb-0 caption roster-name" :class="awayHeaderClass">
          <span v-if="away">
            <router-link :to="{ name: 'roster', params: { leagueId: leagueId, rosterId: away.id } }">
              {{ away.name }}
            </router-link>
          </span>
          <span v-else>TBD</span>
        </v-col>
      </v-row>

      <v-row>
        <v-col class="py-0 text-h4 score" :class="awayScoreClass">
          <score :score="awayScore" />
        </v-col>
      </v-row>

      <v-row>
        <v-col class="py-0 grey--text">
          <score v-if="enableProjections" :score="awayProjection" />
        </v-col>
      </v-row>

      <v-row v-if="showMatchupProgress && away">
        <v-col>
          <matchup-progress :roster="away" :reverse="true" :leagueId="leagueId" class="pr-1" />
        </v-col>
      </v-row>
    </v-col>

    <v-col cols="2" class="text-center">
      <v-row>
        <v-col class="pb-0">vs</v-col>
      </v-row>
    </v-col>

    <v-col cols="5" class="roster-name pr-4 text-left">
      <v-row>
        <v-col class="pb-0 caption roster-name" :class="homeHeaderClass">
          <span v-if="home">
            <router-link :to="{ name: 'roster', params: { leagueId: leagueId, rosterId: home.id } }">
              {{ home.name }}
            </router-link>
          </span>
          <span v-else>TBD</span>
        </v-col>
      </v-row>

      <v-row>
        <v-col class="py-0 text-h4" :class="homeScoreClass">
          <score :score="homeScore" />
        </v-col>
      </v-row>

      <v-row>
        <v-col class="py-0 grey--text">
          <score v-if="enableProjections" :score="homeProjection" />
        </v-col>
      </v-row>

      <v-row v-if="showMatchupProgress && home">
        <v-col>
          <matchup-progress :roster="home" :reverse="false" :leagueId="leagueId" class="pr-1'" />
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import { rosterProjection } from "../../../api/110yards/projection"
import { calculateMultiple, getRosterScoreRef } from "../../../modules/scoring"
import Score from "../../Score.vue"
import MatchupProgress from "./MatchupProgress.vue"

export default {
  components: { Score, MatchupProgress },

  props: {
    away: { type: Object, required: false },
    home: { type: Object, required: false },
    isCurrentWeek: { type: Boolean, required: true },
    enableProjections: { type: Boolean, required: false, default: false },
    weekNumber: { required: true },
  },

  data() {
    return {
      awayPlayers: null,
      homePlayers: null,
      awayProjection: null,
      homeProjection: null,
    }
  },

  computed: {
    season() {
      return this.$root.currentSeason
    },

    leagueId() {
      return this.$root.leagueId
    },

    awayScore() {
      return this.awayPlayers ? calculateMultiple(this.$root.leagueScoringSettings, this.awayPlayers) : 0
    },

    homeScore() {
      return this.homePlayers ? calculateMultiple(this.$root.leagueScoringSettings, this.homePlayers) : 0
    },

    awayHeaderClass() {
      return this.awayScore >= this.homeScore ? "font-weight-black" : ""
    },

    awayScoreClass() {
      return this.awayScore >= this.homeScore ? "" : "grey--text"
    },

    homeHeaderClass() {
      return this.homeScore >= this.awayScore ? "font-weight-black" : ""
    },

    homeScoreClass() {
      return this.homeScore >= this.awayScore ? "" : "grey--text"
    },

    showMatchupProgress() {
      return this.isCurrentWeek && this.$root.enableMatchupProgress
    },
  },

  methods: {},

  watch: {
    away: {
      immediate: true,
      async handler(away) {
        if (away) {
          this.$bind("awayPlayers", getRosterScoreRef(this.season, this.weekNumber, away))

          this.awayProjection = await rosterProjection(this.leagueId, away.id)
        }
      },
    },

    home: {
      immediate: true,
      async handler(home) {
        if (home) {
          this.$bind("homePlayers", getRosterScoreRef(this.season, this.weekNumber, home))

          this.homeProjection = await rosterProjection(this.leagueId, home.id)
        }
      },
    },
  },
}
</script>