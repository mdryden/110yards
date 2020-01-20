<template>
  <div class="col-md-12">
    <table class="table">
      <tr v-for="manager in managers" :key="manager.uid">
        <td>{{ manager.name }}</td>
        <td class="text-right">
          <!-- TODO: apply rules - can't remove once league has started -->
          <button
            class="btn btn-default"
            v-if="manager.uid != uid"
            v-on:click="confirmRemoval(manager)"
          >
            Remove
          </button>
        </td>
      </tr>
    </table>
  </div>
</template>

<script lang="ts">
import Vue from "vue"
import { firestore } from "../../modules/firebase"
import * as leagueService from "../../api/110yards/league"

export default Vue.extend({
  name: "manage-teams",
  props: ["leagueId"],
  data() {
    return {
      managers: [],
    }
  },
  computed: {
    uid() {
      return this.$store.state.uid
    },
    currentUser() {
      return this.$store.state.currentUser
    },
  },
  methods: {
    removeManager(manager) {
      leagueService.removeManager(this.currentUser, this.leagueId, manager.uid)
    },
    async confirmRemoval(manager) {
      let remove = confirm("Remove " + manager.name + "from this league?")
      if (remove) await this.removeManager(manager)
    },
  },
  watch: {
    leagueId: {
      immediate: true,
      async handler(leagueId) {
        if (leagueId == null) return

        try {
          await this.$bind(
            "managers",
            firestore
              .collection("league")
              .doc(leagueId)
              .collection("managers"),
          )
        } catch (exception) {
          this.$eventBus.$emit("exception", exception)
        }
      },
    },
  },
})
</script>
