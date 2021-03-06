import Vue from "vue"
import Vuex from "vuex"
import { firestore } from "../firebase"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentUser: null,
    isAnonymous: true,
    uid: null,
    currentLeagueId: null,
    currentRoles: [],
    isAdmin: false,
    systemState: null,
  },
  mutations: {
    logIn(state, data) {
      state.currentUser = data.user
      state.isAnonymous = false
      state.uid = data.user.uid
      state.currentRoles = data.roles || []
      state.isAdmin = state.currentRoles.includes("ADMIN")
      state.systemState = data.systemState
    },
    logOut(state) {
      state.currentUser = null
      state.isAnonymous = true
      state.uid = null
      state.isAdmin = false
      state.currentRoles = []
    },
    setCurrentLeagueId(state, leagueId) {
      state.currentLeagueId = leagueId
    },
  },
  actions: {
    async updateUser({ commit }, user) {
      if (user) {
        let roles = (await firestore.doc(`user_roles/${user.uid}`).get()).data()
        let systemState = (await firestore.doc("admin/state").get()).data()

        // undefined for most users
        if (roles) {
          roles = roles.roles
        }

        commit("logIn", { user: user, roles: roles, systemState: systemState })
      } else {
        commit("logOut")
      }
    },
    loadLeague({ commit, state }, leagueId) {
      let changingLeague = leagueId !== state.currentLeagueId

      if (changingLeague) {
        console.debug(`Loading league ${leagueId}`)
        commit("setCurrentLeagueId", leagueId)
      }
    },
  },
  modules: {},
  getters: {
    user(state) {
      return state.user
    },
  },
})
