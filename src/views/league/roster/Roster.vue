<template>
  <div class="roster">
    <h3 v-if="manager">{{ manager.name }}</h3>
    <lineup :roster="roster" :leagueId="leagueId" :includeProjection="true" />
  </div>
</template>

<script>
import { firestore } from "../../../modules/firebase"
import Lineup from "../../../components/league/roster/Lineup"

export default {
  name: "roster",
  components: {
    Lineup,
  },
  props: {
    leagueId: String,
    rosterId: String,
  },
  data() {
    return {
      roster: {},
      manager: {},
      rosterConfig: {},
    }
  },
  computed: {
    currentWeek() {
      return this.$store.state.systemState.current_week
    },
  },
  methods: {
    bindRoster(leagueId, rosterId) {
      let ref = firestore
        .collection("league")
        .doc(leagueId)
        .collection("rosters")
        .doc(rosterId)

      this.$bind("roster", ref)
    },
    bindManager(leagueId, rosterId) {
      let ref = firestore
        .collection("league")
        .doc(leagueId)
        .collection("managers")
        .doc(rosterId)

      this.$bind("manager", ref)
    },
  },
  watch: {
    leagueId: {
      immediate: true,
      handler(leagueId) {
        if (leagueId && this.rosterId) {
          this.bindRoster(leagueId, this.rosterId)
          this.bindManager(leagueId, this.rosterId)
        }
      },
    },
    rosterId: {
      immediate: true,
      handler(rosterId) {
        if (rosterId && this.leagueId) {
          this.bindRoster(this.leagueId, rosterId)
          this.bindManager(this.leagueId, rosterId)
        }
      },
    },
  },
}
</script>
