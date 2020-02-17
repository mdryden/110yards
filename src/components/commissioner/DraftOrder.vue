<template>
  <div class="draft-order">
    <form ref="form">
      <div v-for="manager in managers" :key="manager.uid" class="form-group">
        <label class="control-label">{{ manager.name }}</label>
        <select class="form-control" v-model="league.draft_order[manager.uid]">
          <option></option>
          <option
            v-for="number in getPickNumbers()"
            :key="number"
            :value="number"
            >{{ number }}</option
          >
        </select>
      </div>
    </form>
  </div>
</template>

<script>
import { firestore } from "../../modules/firebase"
import _ from "lodash"

export default {
  name: "draft-order",
  components: {},
  props: {
    league: Object,
  },
  data() {
    return {
      managers: [],
    }
  },
  computed: {},
  methods: {
    getPickNumbers() {
      return _.range(1, this.managers.length + 1)
    },
  },
  watch: {
    league: {
      immediate: true,
      handler(league) {
        if (!league) return

        let ref = firestore
          .collection("league")
          .doc(league.id)
          .collection("managers")

        this.$bind("managers", ref)
      },
    },
  },
}
</script>
