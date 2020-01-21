import * as client from "./client"

export const create = async (user, league) => {
  return client.post(user, "/league", league)
}

export const update = async (user, leagueId, options) => {
  return client.put(user, `/league/${leagueId}`, options)
}

export const join = async (user, leagueId, password) => {
  return client.post(user, `/league/${leagueId}/join`, {
    password: password,
  })
}

export const closeRegistration = async (user, leagueId) => {
  return client.put(user, `/league/${leagueId}/registration/close`)
}

export const openRegistration = async (user, leagueId) => {
  return client.put(user, `/league/${leagueId}/registration/open`)
}

export const updateRosterPositions = async (
  user,
  leagueId,
  rosterPositions,
) => {
  return client.put(user, `/league/${leagueId}/positions`, rosterPositions)
}

export const removeManager = async (user, leagueId, managerId) => {
  return client.del(user, `/league/${leagueId}/manager/${managerId}`)
}

export const generateSchedule = async (user, leagueId, options) => {
  return client.put(user, `/league/${leagueId}/schedule`, options)
}
