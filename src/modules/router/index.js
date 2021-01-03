import { createRouter, createWebHistory } from "vue-router"
import { routes } from "./routes"
// import { auth, getCurrentUser } from "../firebase"

const router = createRouter({
  history: createWebHistory(),
  base: process.env.BASE_URL,
  routes,
})

// router.beforeEach(async (to, from, next) => {
//   let ok = checkAuth(to, next)

//   if (ok) {
//     setLeagueId(to)
//     next()
//   }
// })

// async function checkAuth(to, next) {
//   let allowAnonymous = to.matched.some(record => record.meta.anonymous)
//   let ok = allowAnonymous || (await getCurrentUser()) != null

//   if (!ok) {
//     next({ name: "login", query: { returnUrl: to.fullPath } })
//   }

//   return ok
// }

// function setLeagueId(to) {
//   router.app.$store.dispatch("loadLeague", to.params.leagueId)
// }

export default router
