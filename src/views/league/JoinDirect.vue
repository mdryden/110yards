<template>
  <section class="row">
    <div class="col-12">
      <h5>Join league</h5>
      <join-private-form :joinId="joinId" :password="password" />
    </div>
  </section>
</template>

<script>
import JoinPrivateForm from "../../components/league/JoinPrivateForm.vue"
import * as leagueService from "../../api/110yards/league"

export default {
  name: "join-direct",
  props: {
    joinId: String,
  },
  components: {
    JoinPrivateForm,
  },
  computed: {
    currentUser() {
      return this.$store.state.currentUser
    },
    password() {
      return this.$route.query.password
    },
  },
  methods: {
    async trySignup() {
      if (!this.joining && this.joinId && this.currentUser) {
        this.joining = true
        eventBus.$emit("loading-start")

        try {
          await leagueService.join(this.currentUser, this.joinId, this.password)
        } catch (exception) {
          if (exception.message === "Request failed with status code 403")
            alert("League password was incorrect")
          else {
            alert(exception.message)
          }
        }
      }
    },
  },
  watch: {
    joinId: {
      immediate: true,
      async handler(joinId) {
        this.leagueId = joinId
      },
    },
    currentUser: {
      immediate: true,
      async handler(currentUser) {
        //await this.trySignup()
      },
    },
  },
  mounted() {},
}
</script>
