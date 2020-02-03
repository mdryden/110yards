<template>
  <div>
    <div class="row" v-if="!enoughTeams">
      <div class="col-md-12 alert-warning">
        League must have an even number of teams.
      </div>
    </div>

    <div class="row" v-if="enoughTeams">
      <form ref="form" @submit.prevent="submit()">
        <div class="col-12">
          <h4>League roster settings</h4>
          <div class="form-group">
            <label># of playoff teams:</label>
            <select
              class="form-control"
              v-model.number="form.playoffType"
              required
            >
              <option value=""></option>
              <option
                v-for="type in eligiblePlayoffTypes"
                :key="type.id"
                :value="type.id"
                >{{ type.name }}</option
              >
            </select>
          </div>
          <div class="form-group">
            <label>First playoff week:</label>
            <select
              class="form-control"
              v-model="form.firstPlayoffWeek"
              required
            >
              <option value=""></option>
              <option
                v-for="x in weekCounts"
                :key="x"
                v-bind:class="{ ideal: isIdeal(x) }"
                :value="x"
                >{{ x }}</option
              >
            </select>
            <small class="info"
              >Weeks which result in an equal number of games between all teams
              are in bold.</small
            >
          </div>

          <div class="form-group" v-if="canUseLoserPlayoff()">
            <label class="control-label"
              >Enable loser playoff?
              <small class="info"
                >(A single playoff matchup between the bottom two teams in the
                league)</small
              ></label
            >
            <div class="form-check">
              <label class="checkbox-inline">
                <input
                  type="checkbox"
                  v-model="form.enableLoserPlayoff"
                  class="form-check-input"
                />Yes
              </label>
            </div>
          </div>
          <button type="submit" class="btn btn-default">
            Lock registration and generate schedule
          </button>
          <saved-indicator :saved="saved" />
        </div>
      </form>
    </div>

    <div class="row" v-if="hasSchedule">
      <table class="table">
        <tr>
          <th>Week</th>
          <th v-for="x in matchupsPerWeek" :key="x">Matchup {{ x }}</th>
        </tr>
        <tr v-for="week in schedule" :key="week.week_number">
          <td>{{ week.week_number }}</td>
          <td v-for="(matchup, index) in week.matchups" :key="index">
            <span v-if="matchup.type == 'regular'"
              >{{ matchup.away.name }} @ {{ matchup.home.name }}</span
            >
            <span v-if="matchup.type != 'regular'">{{ matchup.type }}</span>
          </td>
          <!--<td v-if="matchup.type == 'regular'">
            {{ matchup.away_name }} @ {{ matchup.home_name }}
          </td>
          <td v-if="matcup.type != 'regular'">{{ matchup.type }}</td> -->
        </tr>
      </table>
    </div>
  </div>
</template>

<style scoped>
option.ideal {
  font-weight: bold;
}
</style>

<script>
import _ from "lodash"
import { firestore } from "../../modules/firebase"
import * as leagueService from "../../api/110yards/league"
import SavedIndicator from "../SavedIndicator"

// TODO: move some of the logic in these methods into a service object

export default {
  name: "schedule",
  components: {
    SavedIndicator,
  },
  props: {
    leagueId: String,
  },
  data() {
    return {
      league: {},
      schedule: [],
      managers: [],
      playoffTypes: [],
      form: {
        playoffType: null,
        firstPlayoffWeek: 0,
        enableLoserPlayoff: false,
      },
      saved: false,
    }
  },
  computed: {
    hasSchedule() {
      return this.schedule.length > 0
    },

    enoughTeams() {
      return this.managers.length % 2 == 0
    },

    eligiblePlayoffTypes() {
      return this.playoffTypes.filter(x => x.id <= this.managers.length)
    },

    weekCounts() {
      const lastWeek = 21
      if (this.form.playoffType == null) return null

      let counts = _.range(1, lastWeek + 1).filter(
        week => week >= this.managers.length, //&&
        // week + this.form.playoffType.weeks <= lastWeek,
      )
      return counts
    },

    matchupsPerWeek() {
      return this.managers.length / 2
    },
  },
  methods: {
    isIdeal(x) {
      return (x - 1) % (this.managers.length - 1) == 0
    },

    canUseLoserPlayoff() {
      let canUse = this.form.playoffType && this.form.playoffType.id > 3

      if (!canUse && this.form.enableLoserPlayoff)
        this.form.enableLoserPlayoff = false

      return canUse
    },

    submit() {
      if (this.$refs.form.checkValidity()) {
        this.save()
      } else {
        this.$refs.form.reportValidity()
      }
    },

    async save() {
      let user = this.$store.state.currentUser
      let options = {
        playoffType: this.form.playoffType,
        firstPlayoffWeek: this.form.firstPlayoffWeek,
        enableLoserPlayoff: this.form.enableLoserPlayoff,
      }

      await leagueService.generateSchedule(user, this.leagueId, options)
      this.saved = true
    },

    bindSchedule(leagueId) {
      this.$bind(
        "schedule",
        firestore
          .collection("league")
          .doc(leagueId)
          .collection("weeks"),
      )
    },

    bindManagers(leagueId) {
      this.$bind(
        "managers",
        firestore.collection(`league/${leagueId}/managers`),
      )
    },

    bindLeague(leagueId) {
      this.$bind("league", firestore.doc(`league/${leagueId}`))
    },

    bindPlayoffTypes() {
      this.$bind("playoffTypes", firestore.collection(`playoff-types`))
    },
  },
  watch: {
    leagueId: {
      immediate: true,
      handler(leagueId) {
        if (leagueId == null) return

        this.bindLeague(leagueId)
        this.bindSchedule(leagueId)
        this.bindManagers(leagueId)
      },
    },

    league: {
      immediate: true,
      handler(league) {
        if (league == null) return
        this.form.playoffType = league.playoffType
        this.form.firstPlayoffWeek = league.firstPlayoffWeek
        this.form.enableLoserPlayoff = league.enableLoserPlayoff
      },
    },
  },

  mounted: function() {
    this.bindPlayoffTypes()
  },
}
</script>
