<template>
  <div class="player-list">
    <div class="row player-tools">
      <div class="col-sm-12 players-filter">
        <div class="form-inline">
          <span>Filter by position:</span>
          <button
            v-for="(position, index) in positions"
            :key="index"
            type="button"
            v-on:click="togglePositionFilter(position)"
            class="btn btn-sm position-toggle"
            :class="{
              'btn-default': filterActive(position),
              'btn-outline-default': !filterActive(position),
            }"
            :data-position="position"
          >
            {{ position }}
          </button>
          <button
            type="button"
            class="btn btn-default btn-sm"
            id="freeAgentsToggle"
          >
            Free Agents
          </button>
        </div>
      </div>

      <!-- <div class="col-sm-6 players-filter-owners">
        <div class>
          @*Include owned players:
          <input class type="checkbox" id="includeOwned" value="@((bool)ViewBag.IncludeOwned)" />*@
        </div>
      </div>-->
    </div>
    <div class="row">
      <h2>Players</h2>
      <table
        v-if="players"
        id="playersTable"
        class="table datatable"
        data-page-length="10"
        data-auto-width="false"
        data-searching="true"
        data-length-change="true"
        data-ordering="[[0, 'asc'], [1, 'asc']]"
        data-column-defs="[{ 'visible': false, 'targets': 0 },{ 'visible': false, 'targets': 1 },{ 'visible': false, 'targets': 2 }]"
      >
        <thead>
          <tr>
            <th>Last</th>
            <th>First</th>
            <th class="free-agent">
              <!-- free agent -->
            </th>
            <th></th>
            <th>Player</th>
            <th>Opp</th>
            <th class="position">Pos</th>
            <th class="owner">Owner</th>
            <th>GP</th>
            <th>Rk</th>
            <th>Points</th>
            <th>Avg</th>
            <th class="detail QB">Passes</th>
            <th class="detail QB">Comp</th>
            <th class="detail QB">Yards</th>
            <th class="detail QB">Int</th>
            <th class="detail QB">TD</th>

            <th class="detail QB RB WR">Rushes</th>
            <th class="detail QB RB WR">Yards</th>
            <th class="detail QB RB WR">TD</th>

            <th class="detail RB WR">Catches</th>
            <th class="detail RB WR">Targets</th>
            <th class="detail RB WR">Yards</th>
            <th class="detail RB WR">TD</th>

            <th class="detail QB RB WR">Convert(2)</th>
            <!-- <th class="detail QB RB WR">FumblesLost</th> -->

            <th class="detail K">Convert(1)</th>
            <th class="detail K">Punt Sgl</th>
            <th class="detail K">Kickoff Sgl</th>
            <th class="detail K">FG Make</th>
            <th class="detail K">FG Miss</th>
            <th class="detail K">FG Miss (1)</th>

            <th class="detail DB RB WR">Kick Ret Yards</th>
            <th class="detail DB RB WR">TD</th>
            <th class="detail DB RB WR">Punt Ret Yards</th>
            <th class="detail DB RB WR">TD</th>
            <th class="detail DB RB WR">FG Ret Yards</th>
            <th class="detail DB RB WR">TD</th>

            <th class="detail LB DL DB">Tackles</th>
            <th class="detail LB DL DB">Sacks</th>
            <th class="detail LB DL DB">Int</th>
            <th class="detail LB DL DB">FF</th>
            <th class="detail LB DL DB">FR</th>
            <!-- @*<th class="detail LB DL DB">TD</th>*@ -->
            <th class="detail LB DL DB">Pass Def</th>
            <!-- @*<th class="detail LB DL DB">Blk Kick</th>*@ -->
            <th class="detail LB DL DB">Safety</th>
          </tr>
        </thead>
        <tr
          v-for="player in players"
          :key="player.id"
          v-show="visible(player)"
          class="player-row"
          :class="[
            {
              'free-agent': !player.owned,
              'my-player': player.ownerId == uid,
            },
            player.position,
          ]"
        >
          <td>{{ player.last_name }}</td>
          <td>{{ player.first_name }}</td>
          <td>{{ player.owned ? "N" : "Y" }}</td>
          <td>
            <!-- <partial name="PlayerActions" model="player" /> -->
          </td>
          <td>
            <!--@Url.PlayerLink(player) @Html.PlayerStatus(player.InactiveType)-->
          </td>
          <td>{{ player.opponent }}</td>
          <td>{{ player.position }}</td>
          <td>{{ player.owner }}</td>
          <td>{{ player.games_played }}</td>
          <td>{{ player.rank }}</td>
          <td>{{ player.season_score }}</td>
          <td>{{ player.season_average }}</td>

          <td>{{ player.season_totals.pass_attempts }}</td>
          <td>{{ player.season_totals.pass_completions }}</td>
          <td>{{ player.season_totals.pass_yards }}</td>
          <td>{{ player.season_totals.PassInterceptions }}</td>
          <td>{{ player.season_totals.PassTouchdowns }}</td>

          <td>{{ player.season_totals.RushAttempts }}</td>
          <td>{{ player.season_totals.RushYards }}</td>
          <td>{{ player.season_totals.RushTouchdowns }}</td>

          <td>{{ player.season_totals.Receptions }}</td>
          <td>{{ player.season_totals.Targets }}</td>
          <td>{{ player.season_totals.ReceivingYards }}</td>
          <td>{{ player.season_totals.ReceivingTouchdowns }}</td>

          <td>{{ player.season_totals.Convert2Scores }}</td>
          <!-- <td>{{ player.season_totals.FumblesLost }}</td> -->

          <td>{{ player.season_totals.Convert1Scores }}</td>
          <td>{{ player.season_totals.PuntSingles }}</td>
          <td>{{ player.season_totals.KickoffSingles }}</td>
          <td>{{ player.season_totals.FieldGoalMakes }}</td>
          <td>{{ player.season_totals.FieldGoalMisses }}</td>
          <td>{{ player.season_totals.FieldGoalSingles }}</td>

          <td>{{ player.season_totals.KickReturnYards }}</td>
          <td>{{ player.season_totals.KickReturnTouchdowns }}</td>
          <td>{{ player.season_totals.PuntReturnYards }}</td>
          <td>{{ player.season_totals.PuntReturnTouchdowns }}</td>
          <td>{{ player.season_totals.MissedFieldGoalReturnYards }}</td>
          <td>{{ player.season_totals.MissedFieldGoalReturnTouchdowns }}</td>

          <td>{{ player.season_totals.DefensiveTackles }}</td>
          <td>{{ player.season_totals.Sacks }}</td>
          <td>{{ player.season_totals.Interceptions }}</td>
          <td>{{ player.season_totals.FumblesForced }}</td>
          <td>{{ player.season_totals.FumblesRecovered }}</td>
          <!-- <td>{{ player.season_totals.DefensiveTouchdowns }}</td> -->
          <td>{{ player.season_totals.PassesDefensed }}</td>
          <!-- <td>{{ player.season_totals.BlockedKicks }}</td> -->
          <td>{{ player.season_totals.Safeties }}</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import { firestore } from "../../modules/firebase"

export default {
  name: "player-list",
  props: {
    leagueId: null,
  },
  data() {
    return {
      players: [],
      positions: ["QB", "RB", "WR"], //todo bind,
      filterPositions: [],
    }
  },
  computed: {
    uid() {
      return this.$store.state.uid
    },
  },
  methods: {
    visible(player) {
      let positionMatch =
        this.filterPositions.length == 0 ||
        this.filterPositions.includes(player.position)
      // todo: free agent filtering
      return positionMatch
    },
    togglePositionFilter(position) {
      if (this.filterPositions.includes(position)) {
        this.filterPositions.pop(position)
      } else {
        this.filterPositions.push(position)
      }
    },
    filterActive(position) {
      return this.filterPositions.includes(position)
    },
  },
  watch: {
    leagueId: {
      immediate: true,
      handler(leagueId) {
        // todo: use league id in binding
        let ref = firestore.collection("player")
        this.$bind("players", ref)
      },
    },
  },
}
</script>
