<template>
  <div class="player-link">
    <router-link :to="{ name: 'player', params: { id: player.id } }">{{
      player.name
    }}</router-link>
    <span class="player-status" :v-if="playerStatus">
      {{ playerStatus }}
    </span>
  </div>
</template>

<script>
import PlayerStatus from "./PlayerStatus.vue"

export default {
  name: "player-link",
  components: {
    PlayerStatus,
  },
  props: {
    player: Object,
  },
  computed: {
    status() {
      return player.status
    },
  },
}
</script>
