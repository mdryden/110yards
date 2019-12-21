<template>
  <div class="row">
    <p class="info">
      Quarterback, running back and kicker slots are capped at 1 maximum, for
      gameplay reasons.
    </p>
    <div class="col-md-6 col-sm-12">
      <form ref="form">
        <table class="table">
          <thead>
            <tr>
              <th>Position</th>
              <th>Count</th>
              <th></th>
            </tr>
          </thead>
          <tr v-for="position in startingPositions" :key="position.id">
            <th>{{ position.name }}</th>
            <td>
              <input type="number" class="form-control" />
            </td>
            <td>{{ position.description }}</td>
          </tr>

          <!-- todo: non-starting spots -->
        </table>

        <button class="btn btn-default">Save changes</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "rosters",
  props: {
    leagueId: String,
  },
  data() {
    return {
      startingPositions: [
        {
          id: "qb",
          name: "Quarterback",
        },
        {
          id: "rb",
          name: "Runningback",
        },
        {
          id: "flex",
          name: "Flex",
          description: "Accepts offensive and defensive flex",
        },
      ],
      nonStartingPositions: [],
    }
  },
}
</script>
