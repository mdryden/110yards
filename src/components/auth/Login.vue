<template>
  <div class="login">
    <div class="row justify-content-center">
      <div class="col-10 col-md-8 col-lg-6">
        <h4>Log in to your account</h4>
        <section id="loginForm">
          <form ref="form" @submit.prevent="login">
            <div class="form-group">
              <input
                type="text"
                class="form-control"
                v-model="email"
                placeholder="Email"
                autocomplete="email"
                required
              />
            </div>
            <div class="form-group">
              <input
                type="password"
                class="form-control"
                v-model="password"
                placeholder="Password"
                autocomplete="current-password"
                required
              />
            </div>
            <div class="form-group">
              <button type="submit" class="btn btn-primary btn-block">Log in</button>
            </div>
          </form>
        </section>

        <p class="text-center">OR</p>

        <social />

        <p class="text-center">
          <router-link to="/forgotpassword">Forgot your password?</router-link>
        </p>
        <p class="text-center">
          Not signed up yet?
          <router-link to="/signup">Sign Up</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { auth } from "../../modules/firebase"
import Social from "./Social"

export default {
  name: "login",
  props: {
    returnUrl: String,
  },
  components: {
    Social,
  },
  data() {
    return {
      email: "",
      password: "",
    }
  },
  methods: {
    async login() {
      try {
        let user = await auth.signInWithEmailAndPassword(
          this.email,
          this.password,
        )

        let target = this.returnUrl || "/"

        this.$router.replace(target)
      } catch (exception) {
        console.error(exception.message)
        alert(exception.message)
      }
    },
  },
  submit() {
    if (this.$refs.form.checkValidity()) {
      this.login()
    } else {
      this.$refs.form.reportValidity()
    }
  },
}
</script>

<style scoped>
#socialLogins {
  margin-bottom: 1rem;
}
</style>