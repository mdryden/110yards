<script type="ts">
import router from "page"

import Home from "./components/Home.svelte"
import About from "./components/About.svelte"

let page = Home
let params;

router("/", () => (page = Home))
router("/about", () => (page = About))

export function start() {
  router.start()
}
</script>

<svelte:component this="{page}" params="{params}" />
