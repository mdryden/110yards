import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentUser: null,
    isAnonymous: true,
    uid: null,
    currentLeagueId: null,
    currentLeague: null,
  },
  mutations: {
    logIn(state, data) {
      state.currentUser = data
      state.isAnonymous = false
      state.uid = data.uid
    },
    logOut(state) {
      state.currentUser = null
      state.isAnonymous = true
      state.uid = null
    },
    setCurrentLeagueId(state, leagueId) {
      state.currentLeagueId = leagueId
    },
  },
  actions: {
    updateUser({ commit }, user) {
      if (user) {
        commit("logIn", user)
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
