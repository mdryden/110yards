<script type="ts">
  import router from "page"

  import Home from "./components/Home.svelte"
  import FAQ from "./components/FAQ.svelte"
  import Footer from "./components/Footer.svelte"

  let page = Home
  let params = null

  router("/", () => (page = Home))
  router("/faq", () => (page = FAQ))
  router("/admin", () => (page = Home))
  router("/login", () => (page = Home))
  router("/league/:leagueId", () => (page = Home))
  router("/league/:leagueId/players", () => (page = Home))
  router("/league/:leagueId/roster/:rosterId", () => (page = Home))
  router.start()

  import NavBar from "./components/NavBar.svelte"
</script>

<main>
  <NavBar />

  <svelte:component this={page} {params} />

  <Footer />
</main>
