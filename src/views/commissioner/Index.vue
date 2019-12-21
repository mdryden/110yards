<template>
  <div v-if="league != null">
    <h5 class="brand">Commmissioner Tools</h5>

    <div class="row">
      <div class="col-md-12">
        <a href="#" @click.prevent="registration()" :league="league"
          >Registration</a
        >&nbsp;|
        <a href="#" @click.prevent="manageTeams()">Manage Teams</a>&nbsp;|
        <a href="#" @click.prevent="leagueOptions()">League options</a>&nbsp;|
        <a href="#" @click.prevent="rosters()">Roster options</a>&nbsp;|
        <a href="#">Schedule settings</a>
        <!-- <partial name="BeginDraftButton" model="@Model.League" /> -->
      </div>
    </div>

    <hr />
    <registration v-if="view == 'registration'" :league="league" />
    <manage-teams v-if="view == 'manage-teams'" :leagueId="leagueId" />
    <league-options v-if="view == 'league-options'" :league="league" />
    <rosters v-if="view == 'rosters'" :leagueId="leagueId" />
    <hr />

    <div class="row" v-if="!league.isLocked"></div>

    <div class="row" v-if="!league.registrationClosed && !isFull"></div>
  </div>
</template>

<script>
import { firestore } from "../../modules/firebase"
import LeagueOptions from "../../components/commissioner/LeagueOptions"
import ManageTeams from "../../components/commissioner/ManageTeams"
import Registration from "../../components/commissioner/Registration"
import Rosters from "../../components/commissioner/Rosters"

export default {
  name: "commissioner-index",
  components: {
    LeagueOptions,
    ManageTeams,
    Registration,
    Rosters,
  },
  props: ["leagueId"],
  data() {
    return {
      league: null,
      view: "registration",
    }
  },
  computed: {
    isFull() {},
  },

  methods: {
    leagueOptions() {
      this.view = "league-options"
    },
    manageTeams() {
      this.view = "manage-teams"
    },
    registration() {
      this.view = "registration"
    },
    rosters() {
      this.view = "rosters"
    },
  },

  watch: {
    leagueId: {
      immediate: true,
      async handler(leagueId) {
        console.log("league id watcher")
        if (leagueId == null) return

        try {
          await this.$bind(
            "league",
            firestore.collection("league").doc(leagueId),
          )
        } catch (exception) {
          this.$eventBus.$emit("exception", exception)
        }
      },
    },
  },
}
</script>

<style scoped>
.active-tool {
  padding-top: 1em;
  padding-bottom: 1em;
}
</style>
