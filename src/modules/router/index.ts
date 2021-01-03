import router from "page"

import FAQ from "../../components/FAQ.svelte"
import Home from "../../views/Home.svelte"
import Login from "../../components/auth/Login.svelte"
import Join from "../../views/league/Join.svelte"
import Create from "../../views/league/Create.svelte"

let page = Home
let params = null

router("/", () => (page = Home))
router("/faq", () => (page = FAQ))
router("/admin", () => (page = Home))
router("/login", () => (page = Login))
router("/league/join", () => (page = Join))
router("/league/create", () => (page = Create))
router("/league/:leagueId", () => (page = Home))
router("/league/:leagueId/players", () => (page = Home))
router("/league/:leagueId/roster/:rosterId", () => (page = Home))
router.start()

export { router, page, params }
