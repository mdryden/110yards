import { createApp } from "vue"
import App from "./App.vue"
import store from "./modules/store"
import router from "./modules/router"

import "./assets/css/site.css"
import "./assets/css/tables.css"
import "./assets/css/buttons.css"
import "./assets/css/team-flair.css"

require("@/assets/scss/main.scss")

const app = createApp(App)
  .use(store)
  .use(router)

app.mount("#app")
