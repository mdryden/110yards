<template>
  <tr>
    <td>{{ spot.short }}</td>
    <td>
      <player-link v-if="player" :player="spot.player" />
    </td>
    <td>
      <span v-if="player">{{ player.next_opponent }}</span>
    </td>
    <td v-if="player" class="text-right">{{ player.score }}</td>
    <td v-if="player && includeProjection" class="text-right">
      {{ player.average }}
    </td>
  </tr>
</template>

<script>
import PlayerLink from "../../../components/player/PlayerLink"

export default {
  name: "lineup-spot",
  components: {
    PlayerLink,
  },
  props: {
    spot: Object,
    player: Object,
    includeProjection: Boolean,
  },
}
</script>
