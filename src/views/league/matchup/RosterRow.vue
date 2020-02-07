<template>
  <tr>
    <td>{{ spot.short_name }}</td>
    <td>
      <player-link :player="spot.player" />
    </td>
    <td>{{ player.next_opponent }}</td>
    <td class="text-right">{{ player.score }}</td>
    <td v-if="includeProjection" class="text-right">{{ player.average }}</td>
  </tr>
</template>

<script>
import PlayerLink from "../../../components/player/PlayerLink"

export default {
  name: "roster-row",
  components: {
    PlayerLink,
  },
  props: {
    spot: Object,
    includeProjection: Boolean,
  },
}
</script>
