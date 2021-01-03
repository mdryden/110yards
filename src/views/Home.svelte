<script type="ts">
  let randomSlogan = "12 > 11"
  let weekNumber = 1 //TODO: state store
</script>

<div class="row">
  <div class="col-md-8 offset-1">
    <section id="leagueOverview">
      <h1 class="brand">110 yards</h1>
      <h5 id="slogan" class="brand">{randomSlogan}</h5>
      <div v-if="hasLeagues">
        <hr />
        <h5>My Teams - Week {weekNumber}</h5>
        <table class="table table-condensed">
          <tbody v-for="league in leagues">
            <tr>
              <td colspan="5" class="league-heading">
                <!-- <router-link
                    :to="{
                      name: 'league',
                      params: { leagueId: league.leagueId },
                    }"
                    >{ league.leagueName }</router-link
                  > -->
              </td>
            </tr>
            <matchup-preview
              :leagueId="league.leagueId"
              :weekNumber="weekNumber"
              :matchup="league.matchup" />
            <!-- <partial name="MatchupRow" model="@matchup.Matchup" />} -->
          </tbody>
        </table>
      </div>
      <h6 v-if="!hasLeagues">Join a league or create a new one!</h6>
      <hr />
      <p>
        <a href="/league/join" class="btn btn-primary">Join a league</a>&nbsp;or
        <a href="/league/create" class="btn btn-default">Create a league</a>
      </p>
      <small v-if="isAnonymous">
        Already have a league?
        <router-link to="/login">Log in</router-link>
      </small>
    </section>
    <!-- @*@Html.Partial("CflNews", Model.News)*@ -->
  </div>
  <div class="col-md-4 hidden-sm hidden-xs">
    <!-- @*@Html.Partial("CflScoreboard")*@ -->
  </div>
</div>
