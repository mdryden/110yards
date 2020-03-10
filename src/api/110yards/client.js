import axios from "axios"
import eventBus from "../../modules/eventBus"

const api110yardsUrl = process.env.VUE_APP_API_110_YARDS_URL

const instance = axios.create({
  baseURL: api110yardsUrl,
})

instance.interceptors.request.use(config => {
  eventBus.$emit("loading-start")
  return config
})

instance.interceptors.response.use(
  response => {
    eventBus.$emit("loading-stop")
    return response
  },
  error => {
    eventBus.$emit("loading-stop")
    if (error.response == undefined) {
      let exception = new Error(error.message)
      eventBus.$emit("nullResponse", exception)
      return
    }

    if (error.response.status >= 400) {
      eventBus.$emit("exception", error)
      return
    }

    let exception = new Error(error.response.data.message)
    exception.response = error.response

    throw exception
  },
)

async function getRequestOptions(user, method, path) {
  let token = await user.getIdToken()

  return {
    url: path,
    method: method,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }
}

export async function get(user, path) {
  let options = await getRequestOptions(user, "get", path)
  return instance(options)
}

export async function post(user, path, data) {
  let options = await getRequestOptions(user, "post", path)
  options.data = data
  let response = await instance(options)

  return response ? response.data : null
}

export async function put(user, path, data) {
  let options = await getRequestOptions(user, "put", path)
  options.data = data
  let response = await instance(options)

  return response ? response.data : null
}

export async function del(user, path) {
  let options = await getRequestOptions(user, "delete", path)
  return instance(options)
}
