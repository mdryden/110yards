import * as client from "./client"

export const create = async (user, league) => {
  return client.post(user, "/league", league)
}

export const update = async (user, league) => {
  return client.put(user, "/league", league)
}

export const join = async (user, leagueId, password) => {
  return client.post(user, "/league/join", {
    leagueId: leagueId,
    password: password,
  })
}

export const closeRegistration = async (user, leagueId) => {
  return client.post(user, `/league/close-registration/${leagueId}`)
}

export const openRegistration = async (user, leagueId) => {
  return client.post(user, `/league/open-registration/${leagueId}`)
}

export const updateRosterPositions = async (
  user,
  leagueId,
  rosterPositions,
) => {
  return client.put(
    user,
    `/league/roster-positions/${leagueId}`,
    rosterPositions,
  )
}
