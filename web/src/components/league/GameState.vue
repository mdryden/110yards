<template>
  <span>
    {{ gameStatus }}
  </span>
</template>

<script>
import { eventStatus } from "../../api/110yards/constants"
import * as formatter from "../../modules/formatter"

export default {
  name: "GameState",
  props: {
    player: {
      type: Object,
      required: false,
    },
    scoreboard: { type: Object, required: true },
    short: { type: Boolean, required: false, default: false },
  },

  computed: {
    gameStatus() {
      if (!this.player) return null
      if (this.player.team.abbreviation == "FA") return "No game"

      let game = this.$root.getGameForTeam(this.player.team.abbreviation, this.scoreboard)

      if (!game) return "Bye week"

      let isHomePlayer = game.teams.home.abbreviation == this.player.team.abbreviation
      let vsMarker = isHomePlayer ? "v" : "@"
      let scoreFor = isHomePlayer ? game.score.home : game.score.away
      let scoreAgainst = isHomePlayer ? game.score.away : game.score.home
      let opponent = this.$root.getOpponent(this.player.team.abbreviation)

      switch (game.event_status.event_status_id) {
        case eventStatus.PreGame: {
          let date = game.date_start.toDate()
          let start = formatter.gameStartTime(date, this.short)
          return `${start} ${vsMarker} ${opponent}`
        }

        case eventStatus.InProgress:
          return `Q${game.event_status.quarter} ${scoreFor}-${scoreAgainst} ${vsMarker} ${opponent}`

        case eventStatus.Final: {
          let won = scoreFor > scoreAgainst
          let lost = scoreFor < scoreAgainst
          let result = won ? "W" : lost ? "L" : "T"
          return `Final ${result} ${scoreFor}-${scoreAgainst} ${vsMarker} ${opponent}`
        }
        case eventStatus.Postponed:
          return game.event_status.name

        default:
          return `${vsMarker} ${opponent} - ${game.event_status.name}`
      }
    },
  },
}
</script>
