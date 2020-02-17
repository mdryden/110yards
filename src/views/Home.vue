<template>
  <div class="row">
    <div class="col-md-8 offset-1">
      <section id="leagueOverview">
        <h1 class="brand">110 yards</h1>
        <h5 id="slogan" class="brand">{{ randomSlogan }}</h5>
        <div v-if="hasLeagues">
          <hr />
          <h5>My Teams - Week {{ weekNumber }}</h5>
          <table class="table table-condensed">
            <tbody v-for="league in leagues" :key="league.leagueId">
              <tr>
                <td colspan="5" class="league-heading">
                  <router-link
                    :to="{
                      name: 'league',
                      params: { leagueId: league.leagueId },
                    }"
                    >{{ league.leagueName }}</router-link
                  >
                </td>
              </tr>
              <matchup-preview
                :leagueId="league.leagueId"
                :weekNumber="weekNumber"
                :matchup="league.matchup"
              />
              <!-- <partial name="MatchupRow" model="@matchup.Matchup" />} -->
            </tbody>
          </table>
        </div>
        <h6 v-if="!hasLeagues">Join a league or create a new one!</h6>
        <hr />
        <p>
          <router-link :to="{ name: 'join-league' }" class="btn btn-primary"
            >Join a league</router-link
          >&nbsp;or
          <router-link :to="{ name: 'create-league' }" class="btn btn-default"
            >Create a league</router-link
          >
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
</template>

<style scoped>
.league-heading {
  text-align: center;
}
</style>

<script>
import { firestore } from "../modules/firebase"
import MatchupPreview from "../components/league/MatchupPreview"

export default {
  name: "home",
  components: {
    MatchupPreview,
  },
  data() {
    return {
      leagues: [],
      leaguesUnsubscribe: null,
    }
  },
  computed: {
    hasLeagues() {
      return this.leagues.length > 0
    },
    isAnonymous() {
      return this.$store.state.isAnonymous
    },
    uid() {
      return this.$store.state.uid
    },
    randomSlogan() {
      return "12 > 11"
    },
    weekNumber() {
      return this.$store.state.systemState.current_week
    },
  },
  methods: {
    bind(uid) {
      let ref = firestore
        .collection("user_leagues")
        .doc(uid)
        .collection("leagues")
        .orderBy("joined")

      this.$bind("leagues", ref)
    },
    unbind(uid) {
      try {
        this.$unbind("leagues")
      } catch (err) {
        // it's fine, probably haven't logged in yet
      }
    },
  },
  watch: {
    uid: {
      immediate: true,
      handler(uid) {
        if (uid != null) {
          this.bind(uid)
        } else {
          this.unbind()
        }
      },
    },
  },
}
</script>
