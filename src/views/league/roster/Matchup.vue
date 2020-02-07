<template>
  <div class="row" v-if="matchup">
    <div class="col-md-12">
      <h4>{{ title }}</h4>
      <hr />
      <div class="row">
        <div class="col-md-6">
          <roster :roster="matchup.away" />
        </div>
        <div class="col-md-6">
          <roster :roster="matchup.home" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Roster from "./Roster.vue"
import { firestore } from "../../../modules/firebase"

export default {
  name: "matchup",
  components: {
    Roster,
  },
  props: {
    matchup,
  },
  data() {
    return {
      matchup: null,
    }
  },
  computed: {
    title() {
      if (!matchup) return

      // todo: format title on server?
      let heading =
        matchup.type == "Regular" ? `Week ${matchup.week_number}` : matchup.type
      return `${heading}: ${matchup.away.name} vs ${matchup.home.name}`
    },
  },
}
</script>
