<script type="ts">
  import { page, params } from "./modules/router"
  import NavBar from "./components/NavBar.svelte"
  import Footer from "./components/Footer.svelte"
</script>

<main>
  <NavBar />

  <svelte:component this={page} {params} />

  <Footer />
</main>
