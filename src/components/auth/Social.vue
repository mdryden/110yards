<template>
  <section id="socialLogins">
    <button
      @click="signInWithGoogle"
      class="btn btn-default btn-block btn-social btn-google"
    >
      <i class="fab fa-google"></i>Continue with Google
    </button>
    <button
      @click="signInWithFacebook"
      class="btn btn-default btn-block btn-social btn-facebook"
    >
      <i class="fab fa-facebook"></i>Continue with Facebook
    </button>
    <button
      @click="signInWithTwitter"
      class="btn btn-default btn-block btn-social btn-twitter"
    >
      <i class="fab fa-twitter"></i>Continue with Twitter
    </button>
  </section>
</template>

<script>
import firebase from "firebase/app"

export default {
  name: "social",
  methods: {
    async signInWithGoogle() {
      let google = new firebase.auth.GoogleAuthProvider()
      await this.socialLogin(google)
    },

    async signInWithFacebook() {
      let facebook = new firebase.auth.FacebookAuthProvider()
      await this.socialLogin(facebook)
    },

    async signInWithTwitter() {
      let twitter = new firebase.auth.TwitterAuthProvider()
      await this.socialLogin(twitter)
    },

    async socialLogin(provider) {
      try {
        let g = new firebase.auth.GoogleAuthProvider()

        await firebase.auth().signInWithPopup(provider)
        this.$router.replace("/")
      } catch (exception) {
        alert("Login failed " + exception.message)
      }
    },
  },
}
</script>
