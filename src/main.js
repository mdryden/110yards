import Vue from "vue"
import App from "./App.vue"
import router from "./modules/router"
import store from "./modules/store"
import eventBus from "./modules/eventBus"
import { firestorePlugin } from "vuefire"
import "firebase/database"
import "firebase/auth"
import "firebase/firestore"

import "bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"

// import "datatables.net-bs4"

import "./assets/css/site.css"
import "./assets/css/tables.css"
import "./assets/css/buttons.css"
import "./assets/css/team-flair.css"

Vue.config.productionTip = false

Vue.use(firestorePlugin)

Vue.prototype.$eventBus = eventBus

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount("#app")
