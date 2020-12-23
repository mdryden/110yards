<script type="ts">
  function signInWithGoogle() {}

  function signInWithFacebook() {}

  function signInWithTwitter() {}
</script>

<section id="socialLogins">
  <button on:click={signInWithGoogle} class="btn btn-default btn-block btn-social btn-google">
    <i class="fab fa-google" />Continue with Google
  </button>
  <button on:click={signInWithFacebook} class="btn btn-default btn-block btn-social btn-facebook">
    <i class="fab fa-facebook" />Continue with Facebook
  </button>
  <button on:click={signInWithTwitter} class="btn btn-default btn-block btn-social btn-twitter">
    <i class="fab fa-twitter" />Continue with Twitter
  </button>
</section>
