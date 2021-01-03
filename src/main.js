import { createApp } from "vue"
import App from "./App.vue"
import PrimeVue from "primevue/config"
import store from "./modules/store"
import router from "./modules/router"

import "primevue/resources/themes/md-dark-indigo/theme.css"
import "./assets/css/site.css"
// import "./assets/css/tables.css"
// import "./assets/css/buttons.css"
// import "./assets/css/team-flair.css"

const app = createApp(App)
  .use(store)
  .use(router)
  .use(PrimeVue)

app.mount("#app")

// todo: put these in another file?
import Button from "primevue/button"
app.component("Button", Button)
