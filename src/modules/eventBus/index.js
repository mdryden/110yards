import Vue from "vue"
import router from "../router"

const eventBus = new Vue()

eventBus.$on("exception", handleException)

export default eventBus

// another file?

function handleException(exception) {
  console.error(exception.message)
  switch (exception.message) {
    case "Missing or insufficient permission.": // firestore rule blocked access to resource
      router.push("/access-denied") // todo: implement this view

    default:
      router.push("/ohno") // todo: implement this view
  }
}
