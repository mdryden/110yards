<template>
  <div v-if="league != null">
    <h5 class="brand">Commmissioner Tools</h5>

    <div class="row">
      <div class="col-md-12">
        <a href="#" @click.prevent="setView('registration')">Registration</a
        >&nbsp;|
        <a href="#" @click.prevent="setView('manage-teams')">Manage Teams</a
        >&nbsp;|
        <a href="#" @click.prevent="setView('league-options')">League options</a
        >&nbsp;|
        <a
          href="#"
          v-if="canSetDraftOrder"
          @click.prevent="setView('draft-order')"
          >Draft Order</a
        ><span v-if="canSetDraftOrder">&nbsp;| </span>
        <a href="#" @click.prevent="setView('rosters')">Roster options</a
        >&nbsp;|
        <a href="#" @click.prevent="setView('schedule')">Schedule settings</a>
      </div>
    </div>

    <hr />
    <registration v-if="view == 'registration'" :league="league" />
    <manage-teams v-if="view == 'manage-teams'" :leagueId="leagueId" />
    <league-options v-if="view == 'league-options'" :league="league" />
    <draft-order v-if="view == 'draft-order'" :league="league" />
    <rosters v-if="view == 'rosters'" :leagueId="leagueId" />
    <schedule v-if="view == 'schedule'" :leagueId="leagueId" />
    <hr />
  </div>
</template>

<script>
import { firestore } from "../../modules/firebase"
import DraftOrder from "../../components/commissioner/DraftOrder"
import LeagueOptions from "../../components/commissioner/LeagueOptions"
import ManageTeams from "../../components/commissioner/ManageTeams"
import Registration from "../../components/commissioner/Registration"
import Rosters from "../../components/commissioner/Rosters"
import Schedule from "../../components/commissioner/Schedule"

export default {
  name: "commissioner-index",
  components: {
    DraftOrder,
    LeagueOptions,
    ManageTeams,
    Registration,
    Rosters,
    Schedule,
  },
  props: ["leagueId"],
  data() {
    return {
      league: null,
      view: "registration",
    }
  },
  computed: {
    canSetDraftOrder() {
      return this.league != null && this.league.draft_type == "Snake"
    },
  },

  methods: {
    setView(view) {
      this.view = view
    },
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
