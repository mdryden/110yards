<template>
  <div class="row">
    <div class="col-md-8" v-if="league != null">
      <h4 class="brand">{{ league.name }}</h4>
      <start-draft :league="league" />
      <!-- <p><a target="_blank" href="@Url.Action("Scoring", "Help", new { id = Model.ScoringSettings.ScoringSettingsId })">@Model.League.ScoringSettings.Name scoring</a></p> -->
      <!-- @if (nextGame != null)
        {
            //string gameTime;
            //if (nextGame.DateStart > DateTime.Now)
            //{
            //	var useDays = timeToNextGame.Value.TotalHours > 24;    v
            //	var useHours = timeToNextGame.Value.TotalMinutes > 60;

            //	var numberFormat = useDays ? @"%d" : (useHours ? @"%h" : @"%m");
            //	var suffix = useDays ? @"days" : (useHours ? @"hours" : @"minutes");

            //	gameTime = $"in {timeToNextGame.Value.ToString(numberFormat)} {suffix}";
            //}
            //else
            //{
            //	gameTime = ", live now";
            //}
            <h6 class="hidden-md hidden-lg">Next game: @nextGame.Team1.Abbreviation vs @nextGame.Team2.Abbreviation <span title="@nextGame.DateStart.ToString("dddd MMMM d, h:mm tt")">@nextGame.DateStart.Remaining("live now")</span></h6>
      }-->
      <hr />
      <div
        id="matchups-carousel"
        class="carousel slide"
        data-ride="carousel"
        data-interval="false"
      >
        <div class="carousel-inner" role="listbox">
          <div
            class="carousel-item"
            :class="isCurrentWeek(week) ? 'active' : null"
            v-for="week in weeks"
            :key="week.week_number"
          >
            <table class="table table-condensed">
              <thead>
                <tr>
                  <th colspan="4">
                    <a
                      v-if="!isFirstWeek(week)"
                      class=""
                      href="#matchups-carousel"
                      role="button"
                      data-slide="prev"
                    >
                      <span
                        class="carousel-control-icon carousel-control-prev-icon"
                        aria-hidden="true"
                      ></span>
                      <span class="sr-only">Previous</span>
                    </a>
                    {{ week.heading }}
                    <a
                      v-if="!isLastWeek(week)"
                      href="#matchups-carousel"
                      role="button"
                      data-slide="next"
                    >
                      <span
                        class="carousel-control-icon carousel-control-next-icon"
                        aria-hidden="true"
                      ></span>
                      <span class="sr-only">Next</span>
                    </a>
                  </th>
                </tr>
              </thead>
              <matchup-preview
                v-for="matchup in week.matchups"
                :key="matchup.id"
                :matchup="matchup"
                :leagueId="leagueId"
              />
            </table>
          </div>
        </div>
      </div>
      <section id="standings">
        <h5>Standings</h5>

        <table class="table table-condensed">
          <thead>
            <tr>
              <th>Team</th>
              <th>Record</th>
              <th>Points For</th>
              <th>Last Week</th>
              <th>Moves</th>
              <th>Waiver</th>
            </tr>
          </thead>

          <tr v-for="manager in managers" :key="manager.uid">
            <td>
              <router-link
                :to="{
                  name: 'roster',
                  params: { leagueId: leagueId, rosterId: manager.uid },
                }"
                >{{ manager.name }}</router-link
              >
              <span v-if="isCommissioner" class="glyphicon glyphicon-star">
                <span class="sr-only">Commissioner</span>
              </span>
            </td>
            <td class="text-center">{{ manager.record }}</td>
            <td class="text-center">{{ manager.pointsFor }}</td>
            <td class="text-center">{{ manager.lastWeek }}</td>
            <td class="text-center">{{ manager.transactionCount }}</td>
            <td class="text-right">${{ manager.waiverBudget }}</td>
          </tr>
        </table>
      </section>
      <!-- TODO: move this into a league nav bar or something -->
      <small v-if="isCommissioner">
        <router-link
          class="nav-item nav-link"
          :to="{ name: 'commissioner', params: { leagueId: leagueId } }"
          >Commissioner Tools</router-link
        >
      </small>
      <!-- @if (Model.Transactions?.Any() == true)
      {
      <hr />
      <partial name="LeagueTransactions" model="@Model.Transactions" />
      }-->
      <!-- @*@Html.Partial("CflNews", Model.News)*@ -->
    </div>
    <!-- <div class="col-md-4 hidden-sm hidden-xs">
      <partial name="CflScoreboard" />
    </div>-->
  </div>
</template>

<style scoped>
.carousel-control-icon {
  height: 0.8em;
}
</style>

<script>
import { firestore } from "../../modules/firebase"
import StartDraft from "../../components/commissioner/StartDraft"
import MatchupPreview from "../../components/league/MatchupPreview"

export default {
  name: "league-index",
  props: ["leagueId"],
  components: {
    StartDraft,
    MatchupPreview,
  },
  data() {
    return {
      league: null,
      managers: [],
      weeks: [],
    }
  },
  computed: {
    isCommissioner() {
      if (this.league == null || this.$store.state.currentUser == null)
        return false

      return this.league.commissioner_id == this.$store.state.currentUser.uid
    },
  },
  methods: {
    isCurrentWeek(week) {
      return week.week_number == 1 // todo: implement
    },
    isFirstWeek(week) {
      return this.weeks != null && this.weeks[0].week_number == week.week_number
    },
    isLastWeek(week) {
      return (
        this.weeks != null &&
        this.weeks[this.weeks.length - 1].week_number == week.week_number
      ) // todo: implement
    },
  },
  watch: {
    leagueId: {
      immediate: true,
      handler(leagueId) {
        if (leagueId == null) return

        this.$bind("league", firestore.collection("league").doc(leagueId))
        this.$bind(
          "managers",
          firestore
            .collection("league")
            .doc(leagueId)
            .collection("managers"),

          this.$bind(
            "weeks",
            firestore
              .collection("league")
              .doc(leagueId)
              .collection("weeks"),
          ),
        )
      },
    },
  },
}
</script>
