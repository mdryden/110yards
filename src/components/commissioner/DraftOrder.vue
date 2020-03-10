<template>
  <div class="draft-order col-6">
    <ol>
      <draggable v-model="draftOrder" @start="drag = true" @end="drag = false">
        <li v-for="element in draftOrder" :key="element.id" class="manager">
          {{ element.name }}
          <span class="fas fa-bars float-right"></span>
        </li>
      </draggable>
    </ol>
    <button type="button" class="btn btn-default" @click="save">
      Update
    </button>
    <saved-indicator :saved="saved" />
  </div>
</template>

<style>
.manager {
  margin: 0.5em;
  padding: 0.5em;
  border: 1px solid var(--bg-color-secondary);
  border-radius: 8px;
  background-color: var(--bg-color-secondary);
  cursor: grabbing;
}

.fas {
  line-height: unset !important;
}
</style>

<script>
import { firestore } from "../../modules/firebase"
import draggable from "vuedraggable"
import SavedIndicator from "../SavedIndicator"
import _ from "lodash"
import * as leagueService from "../../api/110yards/league"

export default {
  name: "draft-order",
  components: {
    draggable,
    SavedIndicator,
  },
  props: {
    league: Object,
  },
  data() {
    return {
      managers: [],
      draftOrder: [],
      saved: false,
    }
  },
  computed: {},
  methods: {
    async save() {
      let user = this.$store.state.currentUser
      let draftOrder = []

      this.draftOrder.forEach(manager => {
        draftOrder.push(manager.id)
      })

      await leagueService.updateDraftOrder(user, this.league.id, draftOrder)
      this.saved = true
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
    managers: {
      immediate: true,
      handler(managers) {
        if (!managers || managers.length == 0) return

        let draftOrder = []

        this.league.draft_order.forEach(id => {
          let manager = managers.filter(m => m.uid == id)[0]
          draftOrder.push({
            name: manager.name,
            id: id,
          })
        })

        this.draftOrder = draftOrder
      },
    },
    draftOrder: {
      deep: true,
      handler(draftOrder) {
        this.saved = false
      },
    },
  },
}
</script>
