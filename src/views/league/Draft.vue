<template>
  <div class="draft">
    <div class="row">
      <div
        class="col-sm-6 col-md-3"
        v-for="draftRoster in draftRosters"
        :key="draftRoster.id"
      >
        <h4>{{ draftRoster.name }}</h4>
        <lineup
          :roster="draftRosters.roster"
          :leagueId="leagueId"
          :includeProjection="false"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { firestore } from "../../modules/firebase"
import Lineup from "../../components/league/roster/Lineup"

export default {
  name: "draft",
  components: {
    Lineup,
  },
  props: {
    leagueId: String,
  },
  data() {
    return {
      draftRosters: [],
    }
  },
  computed: {},
  watch: {
    leagueId: {
      immediate: true,
      handler(leagueId) {
        if (!leagueId) return

        let ref = firestore
          .collection("league")
          .doc(leagueId)
          .collection("draft_roster")

        this.$bind("draftRosters", ref)
      },
    },
  },
}
</script>
