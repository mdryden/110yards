<script type="ts">
  // TODO: move routing into it's own page
  import router from "page"

  import Home from "./components/Home.svelte"
  import About from "./components/About.svelte"

  let page = Home
  let params = null

  router("/", () => (page = Home))
  router("/faq", () => (page = About))
  router("/admin", () => (page = Home))
  router("/login", () => (page = Home))
  router("/league/:leagueId", () => (page = Home))
  router("/league/:leagueId/players", () => (page = Home))
  router("/league/:leagueId/roster/:rosterId", () => (page = Home))
  router.start()

  // end of routing

  import NavBar from "./components/NavBar.svelte"

  export let version = "1.0.0"
  export let lastUpdated = "a while ago"
</script>

<style>
  #footer {
    padding-top: 2em;
    margin: auto;
    width: 50%;
    text-align: center;
    font-size: small;
    color: gray;
  }
</style>

<main>
  <NavBar />

  <svelte:component this={page} {params} />

  <div class="container" id="body" data-version={version}>
    <div id="footer">
      <p>&copy; 2021 Michael Dryden</p>
      <p title="Version {version}">Last release {lastUpdated}</p>
    </div>
  </div>
</main>
