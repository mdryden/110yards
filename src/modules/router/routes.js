import Home from "../../views/Home.vue"
// import DefaultError from "../../views/error/Default.vue"
// import NotAuthorized from "../../views/error/NotAuthorized.vue"

import Login from "../../components/auth/Login.vue"
import Register from "../../components/auth/Register.vue"

import CreateLeague from "../../views/league/Create.vue"
// import LeagueIndex from "../../views/league/Index.vue"
import Join from "../../views/league/Join.vue"
// import JoinDirect from "../../views/league/JoinDirect.vue"
// import Matchup from "../../views/league/roster/Matchup.vue"
// import Roster from "../../views/league/roster/Roster.vue"
// import Draft from "../../views/league/Draft.vue"

// import CommissionerIndex from "../../views/commissioner/Index.vue"

// import Players from "../../views/player/Players.vue"

export const routes = [
  {
    path: "/",
    name: "home",
    component: Home,
    meta: { anonymous: true },
  },
  //   {
  //     path: "/ohno",
  //     name: "error",
  //     component: DefaultError,
  //     meta: { anonymous: true },
  //   },
  //   {
  //     path: "/access-denied",
  //     name: "access-denied",
  //     component: NotAuthorized,
  //     meta: { anonymous: true },
  //   },
  {
    path: "/login",
    name: "login",
    props: route => ({
      returnUrl: route.query.returnUrl,
    }),
    component: Login,
    meta: { anonymous: true },
  },
  {
    path: "/signup",
    name: "signup",
    component: Register,
    meta: { anonymous: true },
  },
  {
    path: "/league/create",
    name: "create-league",
    component: CreateLeague,
  },
  {
    path: "/join",
    name: "join-league",
    component: Join,
  },
  //   {
  //     path: "/join/:joinId",
  //     name: "join-direct",
  //     props: true,
  //     component: JoinDirect,
  //   },
  //   {
  //     path: "/league/:leagueId",
  //     name: "league",
  //     props: true,
  //     component: LeagueIndex,
  //   },
  //   {
  //     path: "/league/:leagueId/week/:weekNumber/matchup/:matchupId",
  //     name: "matchup",
  //     component: Matchup,
  //     props: true,
  //   },
  //   {
  //     path: "/league/:leagueId/roster/:rosterId",
  //     name: "roster",
  //     props: true,
  //     component: Roster,
  //   },
  //   {
  //     path: "/league/:leagueId/players",
  //     name: "league-players",
  //     props: true,
  //     component: Players,
  //   },
  //   {
  //     path: "/league/:leagueId/draft",
  //     name: "draft",
  //     props: true,
  //     component: Draft,
  //   },
  //   {
  //     path: "/commissioner/:leagueId",
  //     name: "commissioner",
  //     props: true,
  //     component: CommissionerIndex,
  //   },
  {
    path: "/admin",
    name: "admin",
    component: null,
  },
  {
    path: "/faq",
    name: "faq",
    component: null,
  },
]
