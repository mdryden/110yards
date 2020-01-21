import Vue from "vue"
import router from "../router"

const eventBus = new Vue()

eventBus.$on("exception", handleException)

export default eventBus

// another file?

function handleException(exception) {
  let message = exception.response ? exception.response.data : exception.message

  switch (exception.message) {
    case "Missing or insufficient permissions.": // firestore rule blocked access to resource
      router.push({ name: "access-denied" }) // todo: implement this view
      break

    default:
      router.push({ name: "error", params: { message: message } })
      break
  }
}
