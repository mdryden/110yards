import { createApp } from "vue"
import App from "./App.vue"
import store from "./modules/store"

import "./assets/css/site.css"
import "./assets/css/tables.css"
import "./assets/css/buttons.css"
import "./assets/css/team-flair.css"

require("@/assets/scss/main.scss")

const app = createApp(App).use(store)

app.mount("#app")
