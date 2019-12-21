<template>
  <div class="row">
    <div class="col-md-8 offset-1">
      <section id="leagueOverview">
        <h1 class="brand">110 yards</h1>
        <h5 class="brand">{{ randomSlogan }}</h5>
        <div v-if="leagues.length > 0">
          <hr />
          <h5>My Teams - Week {{ weekNumber }}</h5>
          <table class="table table-condensed">
            <tbody>
              <tr v-for="league in leagues" :key="league.leagueId">
                <td colspan="4" class="league-heading">
                  <router-link
                    :to="{
                      name: 'league',
                      params: { leagueId: league.leagueId },
                    }"
                    >{{ league.leagueName }}</router-link
                  >
                </td>
              </tr>
              <!-- <partial name="MatchupRow" model="@matchup.Matchup" />} -->
            </tbody>
          </table>
        </div>
        <h6 v-if="matchupsCount == 0">Join a league or create a new one!</h6>
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

<script>
import { firestore } from "../modules/firebase"

export default {
  name: "home",
  data() {
    return {
      matchups: null,
      matchupsCount: 0,
      weekNumber: 0,
      leagues: [],
      hasLeagues: false,
      leaguesUnsubscribe: null,
    }
  },
  computed: {
    isAnonymous() {
      return this.$store.state.isAnonymous
    },
    uid() {
      return this.$store.state.uid
    },
    randomSlogan() {
      return "12 > 11"
    },
  },
  methods: {
    bind(uid) {
      let ref = firestore
        .collection("user_leagues")
        .doc(uid)
        .collection("leagues")

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
