<template>
  <div class="row">
    <div class="col-md-8" v-if="league != null">
      <h4 class="brand">{{ league.name }}</h4>
      <!-- <p><a target="_blank" href="@Url.Action("Scoring", "Help", new { id = Model.ScoringSettings.ScoringSettingsId })">@Model.League.ScoringSettings.Name scoring</a></p> -->
      <!-- @if (nextGame != null)
        {
            //string gameTime;
            //if (nextGame.DateStart > DateTime.Now)
            //{
            //	var useDays = timeToNextGame.Value.TotalHours > 24;
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
      <!-- <div id="matchups-carousel" class="carousel slide" data-ride="carousel" data-interval="false">

            <div class="carousel-inner" role="listbox">
                @foreach (var week in Model.Weeks)
                {
                    var heading = week.Type == WeekType.Regular ? $"Week {week.WeekNumber}" : $"Week {week.WeekNumber} - {week.Type.ToString()}";
                    var activeClass = week.WeekNumber == Model.League.CurrentWeek.WeekNumber ? "active" : "";
                    <div class="item @activeClass">
                        <table class="table table-condensed">
                            <thead>
                                <tr>
                                    <th colspan="4">
                                        @if (week.WeekNumber != Model.Weeks.First().WeekNumber)
                                        {
                                            <a class="" href="#matchups-carousel" role="button" data-slide="prev">
                                                <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
                                                <span class="sr-only">Previous</span>
                                            </a>
                                        }
                                        @heading
                                        @if (week.WeekNumber != Model.Weeks.Last().WeekNumber)
                                        {
                                            <a class="" href="#matchups-carousel" role="button" data-slide="next">
                                                <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
                                                <span class="sr-only">Next</span>
                                            </a>
                                        }
                                    </th>
                                </tr>
                            </thead>
                            @{ var matchupIndex = 0; }
                            @foreach (var matchup in week.Matchups)
                            {
                                ViewBag.Future = week.WeekNumber > Model.League.CurrentWeek.WeekNumber;
                                ViewBag.WeekNumber = week.WeekNumber;
                                ViewBag.LeagueId = Model.League.Id;
                                ViewBag.MatchupIndex = matchupIndex++;
                                <partial name="MatchupRow" model="@matchup" />
                            }
                        </table>
                    </div>
                }
            </div>
      </div>-->
      <section v-if="canStartDraft">
        <partial name="BeginDraftButton" model="Model.League" />
      </section>
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
                :to="{ name: 'roster', params: { leagueId: leagueId, rosterId: manager.uid}}"
              >{{ manager.name }}</router-link>
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
          :to="{ name: 'commissioner', params: {leagueId: leagueId}}"
        >Commissioner Tools</router-link>
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

<script>
import { firestore } from "../../modules/firebase"

export default {
  name: "league-index",
  props: ["leagueId"],
  data() {
    return {
      league: null,
      managers: [],
    }
  },
  computed: {
    canStartDraft() {
      //if (Model.League.DraftState != DraftState.Complete && UserHelper.IsUserCommissioner(User, Model.League))
    },
    isCommissioner() {
      if (this.league == null || this.$store.state.currentUser == null)
        return false

      return this.league.commissioner_id == this.$store.state.currentUser.uid
    },
  },
  watch: {
    leagueId: {
      immediate: true,
      async handler(leagueId) {
        if (leagueId == null) return

        try {
          await this.$bind(
            "league",
            firestore.collection("league").doc(leagueId),
          )
          await this.$bind(
            "managers",
            firestore
              .collection("league")
              .doc(leagueId)
              .collection("managers"),
          )
        } catch (exception) {
          this.$eventBus.$emit("exception", exception)
        }
      },
    },
  },
}
</script>