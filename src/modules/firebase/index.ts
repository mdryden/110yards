import firebase from "firebase/app"
import "firebase/auth"
import "firebase/firestore"

const firebaseApiKey = __process.env.VUE_APP_FIREBASE_API_KEY
const firebaseProject = __process.env.VUE_APP_FIREBASE_PROJECT

console.log(`project: ${firebaseProject}`)

const config = {
  apiKey: firebaseApiKey,
  authDomain: `${firebaseProject}.firebaseapp.com`,
  databaseURL: `https://${firebaseProject}.firebaseio.com`,
  projectId: firebaseProject,
  storageBucket: "",
  messagingSenderId: "",
  appId: "",
}

firebase.initializeApp(config)

export const firestore = firebase.firestore()
export const auth = firebase.auth()

firebase.auth().onAuthStateChanged(user => {
  store.dispatch("updateUser", user)
})

export const getCurrentUser = () => {
  return new Promise((resolve, reject) => {
    const unsubscribe = firebase.auth().onAuthStateChanged(user => {
      unsubscribe()
      resolve(user)
    }, reject)
  })
}
