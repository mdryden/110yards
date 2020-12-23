<script type="ts">
  import Social from "./Social.svelte"
  function login() {}
</script>

<div class="login">
  <div class="row justify-content-center">
    <div class="col-10 col-md-8 col-lg-6">
      <h4>Log in to your account</h4>
      <section id="loginForm">
        <form on:submit|once={login}>
          <div class="form-group">
            <input
              id="email"
              type="text"
              class="form-control"
              v-model="email"
              placeholder="Email"
              autocomplete="email"
              required />
          </div>
          <div class="form-group">
            <input
              id="password"
              type="password"
              class="form-control"
              v-model="password"
              placeholder="Password"
              autocomplete="current-password"
              required />
          </div>
          <div class="form-group">
            <button id="submit" type="submit" class="btn btn-primary btn-block"> Log in </button>
          </div>
        </form>
      </section>

      <p class="text-center">OR</p>

      <Social />

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
