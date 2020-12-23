<script type="ts">
  let leagueId: string = null
  let userId: string = null
  let isAdmin = true // TODO
  let isAnonymous = true // TODO:
</script>

<style>
  .navbar {
    background-color: var(--color-primary);
    background-image: none;
  }
  .navbar img.logo-small {
    height: 40px;
  }
  .navbar-brand {
    margin-top: -8px;
  }
</style>

<nav class="navbar navbar-expand-md navbar-dark">
  <button type="button" class="navbar-toggler" data-toggle="collapse" data-target="#navbar-left">
    <span class="navbar-toggler-icon" />
  </button>
  <a href="/" class="navbar-brand">
    <img
      id="home-link-img"
      class="logo-small"
      src="assets/img/football-white.png"
      alt="110 yards" />
    <label class="sr-only" for="home-link-img">Home</label>
  </a>
  <div id="navbar-left" class="navbar-collapse collapse">
    <div class="nav navbar-nav">
      {#if leagueId}<a href="/league/:leagueId" class="nav-item nav-link">League</a>{/if}

      {#if leagueId && userId}
        <a href="/league/{leagueId}/roster/{userId}" class="nav-item nav-link">My Team</a>
      {/if}

      {#if leagueId}<a href="/league/{leagueId}/players" class="nav-item nav-link">Players</a>{/if}

      <a href="/faq" class="nav-item nav-link">FAQ</a>

      {#if isAdmin}<a href="/admin" class="nav-item nav-link">Admin</a>{/if}
    </div>
    <div class="nav navbar-nav ml-auto">
      {#if isAnonymous}
        <a href="/login" id="login" class="nav-item nav-link">Log in</a>
        <!-- <span class="nav-item navbar-text">{{username}}</span> -->
      {/if}

      {#if !isAnonymous}<a href="/logout" id="logout" class="nav-item nav-link">Log out</a>{/if}
    </div>
  </div>
</nav>
