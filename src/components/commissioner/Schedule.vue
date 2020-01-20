<template>
  <div>
    <div class="row" v-if="!enoughTeams">
      <div class="col-md-12 alert-warning">
        League must have an even number of teams.
      </div>
    </div>

    <div class="row" v-if="enoughTeams">
      <form ref="form" @submit.prevent="submit()">
        <div class="col-md-6 col-sm-12">
          <h4>League roster settings</h4>
          <div class="form-group">
            <label># of playoff teams:</label>
            <select
              class="form-control"
              v-model="playoffType"
              data-required="true"
            >
              <option value=""></option>
              <option
                v-for="type in eligiblePlayoffTypes"
                :key="type"
                :value="type.id"
                >{{ type.name }}</option
              >
            </select>
          </div>
          <div class="form-group">
            <label>First playoff week:</label>
            <select class="form-control" name="FirstPlayoffWeek">
              <option value=""></option>
              <option
                v-for="x in weekCounts"
                :key="x"
                v-bind:class="{ ideal: isIdeal(x) }"
                :value="firstPlayoffWeek"
                >{{ x }}</option
              >
            </select>
            <span class="info"
              >Weeks which result in an equal number of games between all teams
              are in bold.</span
            >
          </div>

          <div
            class="form-group"
            v-if="managerCount > 2 && canUseLoserPlayoff()"
          >
            <label>Enable loser playoff:</label>
            <input
              type="checkbox"
              name="EnableLoserPlayoffs"
              v-model="enableLoserPlayoff"
              value="true"
            />
            <span class="info"
              >Loser playoff is a single playoff matchup between the bottom two
              teams in the league.</span
            >
          </div>
          }
          <button type="submit" class="btn btn-default">
            Lock registration and generate schedule
          </button>
          <partial name="BeginDraftButton" model="CurrentLeague" />
          }
        </div>
      </form>
    </div>

    <div class="row" v-if="schedule.length > 0">
      <table class="table">
        <tr>
          <th>Week</th>
          <th v-for="x in matchupsPerWeek" :key="x">Matchup {{ x }}</th>
        </tr>
        <tr v-for="week in schedule" :key="week.number">
          <td>{{ week.number }}</td>
          <td v-for="matchup in week.matchups" :key="matchup.id"></td>
          <td v-if="matchup.type == 'regular'">
            {{ matchup.away_name }} @ {{ matchup.home_name }}
          </td>
          <td v-if="matcup.type != 'regular'">{{ matchup.type }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import _ from "lodash"

export default {
  name: "schedule",
  props: {
    leagueId: String,
  },
  data() {
    return {
      schedule: {},
      playoffTypes: [],
      managerCount: 8,
      playoffType: 0,
      firstPlayoffWeek: 0,
      enableLoserPlayoff: false,
    }
  },
  computed: {
    enoughTeams() {
      return false
    },
    eligiblePlayoffTypes() {
      return this.playoffTypes.filter(x => x.id <= this.managerCount)
    },
    weekCounts() {
      return _.range(21).filter(x => x.id >= this.managerCount)
    },
    matchupsPerWeek() {
      return this.managerCount / 2
    },
  },
  methods: {
    isIdeal(x) {
      return (x - 1) % (this.managerCount - 1) == 0
    },
    canUseLoserPlayoff() {
      return (
        this.playoffType > this.managerCount &&
        this.playoffType - this.managerCount >= 2
      )
    },
  },
}
</script>
