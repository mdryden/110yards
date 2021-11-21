<template>
  <v-row>
    <v-spacer />
    <v-col cols="12" lg="7">
      <v-card v-if="roster">
        <v-card-text v-if="!editing" class="font-weight-medium d-flex">
          <v-col cols="8" class="pa-0">
            <v-row>
              <v-col class="pl-1 pb-0">
                {{ roster.name }}
                <v-btn
                  class="mt-n1"
                  v-if="canEditName && !editing"
                  icon
                  small
                  title="Edit team name"
                  @click="editing = true"
                >
                  <v-icon small :color="editPencilColor">mdi-lead-pencil</v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="caption pl-1 py-0">{{ roster.record }} | {{ formatRank(roster.rank) }} </v-col>
            </v-row>
            <v-row>
              <v-col class="caption pl-1 py-0"> </v-col>
            </v-row>
          </v-col>

          <v-spacer />

          <v-col cols="3" class="pa-0">
            <v-row>
              <v-col class="pb-0 text-right font-weight-medium">{{ formatScore(score) }}</v-col>
            </v-row>
            <v-row>
              <v-col class="py-0 text-right caption" v-if="projection">Proj. {{ formatScore(projection) }} </v-col>
            </v-row>
          </v-col>
        </v-card-text>

        <v-card-actions v-if="!editing">
          <v-btn class="mr-2" @click="page = 'roster'" :text="page != 'roster'">Lineup</v-btn>
          <v-btn v-if="isOwner" @click="page = 'waivers'" :text="page != 'waivers'">Waiver bids</v-btn>

          <v-spacer />
        </v-card-actions>

        <v-card-text v-if="editing">
          <v-col cols="12">
            <v-form ref="form" @submit.prevent="submit()">
              <app-text-field
                v-if="!roster.name_changes_banned"
                v-model="form.rosterName"
                label="Roster name"
                :rules="rosterNameRules"
                required
              />
              <v-alert type="error" v-if="roster.name_changes_banned"
                >The commissioner has disabled name changes for your team</v-alert
              >
              <app-primary-button v-if="!roster.name_changes_banned" class="mr-2">Save</app-primary-button>
              <app-default-button @click="editing = false">Cancel</app-default-button>
            </v-form>
          </v-col>
        </v-card-text>

        <v-card-text v-if="!editing">
          <lineup
            ref="lineup"
            v-if="roster && league && page == 'roster'"
            :roster="roster"
            :league="league"
            :canEdit="canEditRoster"
          />

          <waivers :roster="roster" :leagueId="leagueId" v-if="isOwner && page == 'waivers'" />
        </v-card-text>

        <v-card-subtitle>
          <v-btn v-if="isCommissioner && !commissionerOverride" @click="commissionerOverride = true"
            >Enter Commissioner Mode</v-btn
          >
          <v-btn v-if="isCommissioner && commissionerOverride" @click="commissionerOverride = false"
            >Exit Commissioner Mode</v-btn
          >
        </v-card-subtitle>
      </v-card>
    </v-col>

    <v-spacer />
  </v-row>
</template>

<style scoped></style>

<script>
import { firestore } from "../../../modules/firebase"
import Lineup from "../../../components/league/roster/Lineup.vue"
import AppTextField from "../../../components/inputs/AppTextField.vue"
import AppPrimaryButton from "../../../components/buttons/AppPrimaryButton.vue"
import { updateRosterName } from "../../../api/110yards/roster"
import { rosterScore } from "../../../api/110yards/score"
import AppDefaultButton from "../../../components/buttons/AppDefaultButton.vue"
import { draftState } from "../../../api/110yards/constants"
import PlayerLink from "../../../components/player/PlayerLink.vue"
import Waivers from "./Waivers.vue"
import * as formatter from "../../../modules/formatter"
import scoreboard from "../../../mixins/scoreboard"

export default {
  name: "roster",
  components: {
    Lineup,
    AppTextField,
    AppPrimaryButton,
    AppDefaultButton,
    PlayerLink,
    Waivers,
  },
  props: {
    leagueId: String,
    rosterId: String,
    inputPage: { type: String, required: false, default: "roster" },
  },
  mixins: [scoreboard],
  data() {
    return {
      page: this.inputPage,
      roster: {},
      league: null,
      editing: false,
      commissionerOverride: false,
      form: {
        rosterName: null,
      },
      rosterNameRules: [v => !!v || "Roster name is required"],
      currentMatchup: null,
      projection: null,
      score: null,
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.currentUser
    },
    currentWeek() {
      return this.$root.state.current_week
    },

    isCommissioner() {
      if (this.league == null || this.$store.state.uid == null) return false

      return this.league.commissioner_id == this.$store.state.uid
    },

    canEdit() {
      let isUsersRoster = this.$store.state.uid == this.rosterId

      return isUsersRoster || (this.isCommissioner && this.commissionerOverride)
    },
    canEditName() {
      return this.canEdit || this.isCommissioner
    },
    editPencilColor() {
      return this.roster.name_changes_banned ? "grey darken-2" : null
    },

    hasBye() {
      return this.roster != null && !this.roster.current_matchup
    },

    waiversActive() {
      return this.$root.state.waivers_active
    },

    isOwner() {
      return this.roster != null && this.roster.id == this.$store.state.uid
    },

    isOwner() {
      return this.roster != null && this.roster.id == this.$store.state.uid
    },

    isCommissioner() {
      if (this.league == null || this.$store.state.currentUser == null) return false

      return this.league.commissioner_id == this.$store.state.currentUser.uid
    },

    canEditRoster() {
      return this.canEdit && this.league != null && this.league.draft_state == draftState.Complete
    },

    currentMatchupStatus() {
      if (this.roster == null) return ""

      if (this.hasBye) return "Bye"

      if (this.currentMatchup == null) return ""

      let isAwayTeam = this.currentMatchup.away && this.currentMatchup.away.id == this.rosterId
      let rosterScore = isAwayTeam ? this.currentMatchup.away_score : this.currentMatchup.home_score
      let opponentScore = isAwayTeam ? this.currentMatchup.home_score : this.currentMatchup.away_score
      let opponentName = isAwayTeam ? this.currentMatchup.home.name : this.currentMatchup.away.name

      return `${rosterScore} - ${opponentScore} vs ${opponentName}`
    },
  },
  methods: {
    formatScore(score) {
      if (score == null || score == undefined) score = 0

      return formatter.formatScore(score)
    },

    formatRank(rank) {
      switch (rank) {
        case 1:
          return "1st"
        case 2:
          return "2nd"
        case 3:
          return "3rd"
        case 4:
        case 5:
        case 6:
        case 7:
        case 8:
          return `${rank}th`
        default:
          return "n/a"
      }
    },

    submit() {
      let valid = this.$refs.form.validate()
      if (!valid) return

      this.save()
    },

    async save() {
      let command = {
        league_id: this.leagueId,
        roster_id: this.rosterId,
        roster_name: this.form.rosterName,
      }

      await updateRosterName(command)

      this.editing = false
    },

    configureBindings(leagueId, rosterId) {
      let leagueRef = firestore.collection("league").doc(leagueId)
      let rosterRef = leagueRef.collection("roster").doc(rosterId)

      this.$bind("league", leagueRef)
      this.$bind("roster", rosterRef)
    },

    async updateScore() {
      if (!this.scoreboard) return

      let rosterInfo = await rosterScore(this.leagueId, this.rosterId)
      this.projection = rosterInfo.projection
      this.score = rosterInfo.score
    },
  },
  watch: {
    leagueId: {
      immediate: true,
      handler(leagueId) {
        if (leagueId && this.rosterId) {
          this.configureBindings(leagueId, this.rosterId)
        }
      },
    },
    rosterId: {
      immediate: true,
      handler(rosterId) {
        if (rosterId && this.leagueId) {
          this.configureBindings(this.leagueId, rosterId)
        }
      },
    },
    editing: {
      handler(editing) {
        if (editing) {
          this.form.rosterName = this.roster.name
        }
      },
    },
    roster: {
      immediate: true,
      handler(roster) {
        if (roster != null && !!this.roster.current_matchup) {
          let collection = firestore.collection(`league/${this.leagueId}/week/${this.currentWeek}/matchup/`)
          let doc = collection.doc(`${this.roster.current_matchup}`)

          this.$bind("currentMatchup", doc)
          this.updateScore()
        }
      },
    },

    scoreboard: {
      immediate: true,
      handler(scoreboard) {
        this.updateScore()
      },
    },
  },
}
</script>