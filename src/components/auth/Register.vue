<template>
  <div class="register">
    <div class="row justify-content-center">
      <div class="col-10 col-md-8 col-lg-6">
        <h4>Create a new account</h4>
        <section id="registerForm">
          <form ref="form" @submit.prevent="submit">
            <div class="form-group">
              <input
                type="text"
                class="form-control"
                v-model="displayName"
                placeholder="Display Name"
                required
                minlength="3"
              />
            </div>
            <div class="form-group">
              <input
                type="text"
                class="form-control"
                v-model="email"
                placeholder="Email"
                required
                minlength="5"
              />
            </div>
            <div class="form-group">
              <input
                type="password"
                class="form-control"
                v-model="password"
                placeholder="Password"
                required
                minlength="6"
              />
            </div>
            <div class="form-group">
              <button type="submit" class="btn btn-primary btn-block">Sign up</button>
            </div>
          </form>
        </section>

        <p class="text-center">OR</p>

        <social />
      </div>
    </div>
  </div>
</template>

<script>
import Social from "./Social"
import { auth } from "../../modules/firebase"

export default {
  name: "login",
  components: {
    Social,
  },
  data() {
    return {
      displayName: "",
      email: "",
      password: "",
    }
  },
  methods: {
    submit() {
      if (this.$refs.form.checkValidity()) {
        this.register()
      } else {
        this.$refs.form.reportValidity()
      }
    },

    async register() {
      try {
        let user = await auth.createUserWithEmailAndPassword(
          this.email,
          this.password,
        )
        await auth.currentUser.updateProfile({
          displayName: this.displayName,
        })

        this.$router.replace("/")
      } catch (error) {
        var errorCode = error.code
        var errorMessage = error.message
        console.error(errorMessage)
        alert(errorMessage)
      }
    },
  },
}
</script>