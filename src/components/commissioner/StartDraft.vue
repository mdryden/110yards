<template>
  <div v-if="isCommissioner" class="draft-button">
    <button
      v-if="canStartDraft"
      v-on:click="startDraft"
      class="btn btn-primary"
    >
      Start Draft
    </button>
    <button
      v-if="canResumeDraft"
      class="btn btn-primary"
      v-on:click="goToDraft"
    >
      Resume Draft
    </button>
  </div>
</template>

<style scoped></style>

<script>
import * as leagueService from "../../api/110yards/league"

export default {
  name: "start-draft",
  props: {
    league: {},
  },
  computed: {
    isCommissioner() {
      if (this.league == null || this.$store.state.uid == null) return false

      return this.league.commissioner_id == this.$store.state.uid
    },
    canStartDraft() {
      return (
        this.isCommissioner &&
        this.league.draft_state == "NotStarted" &&
        this.league.schedule_generated
      )
    },
    canResumeDraft() {
      return this.isCommissioner && this.league.draft_state == "InProgress"
    },
  },

  methods: {
    async startDraft() {
      if (!this.canStartDraft) return

      await leagueService.beginDraft(
        this.$store.state.currentUser,
        this.league.id,
      )

      this.goToDraft()
    },
    goToDraft() {
      this.$router.push({
        name: "draft",
        params: { leagueId: this.league.id },
      })
    },
  },
}
</script>
