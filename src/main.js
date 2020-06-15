import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from "bootstrap-vue"
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from './router'
import {library} from '@fortawesome/fontawesome-svg-core'
import {faLinkedin,faGithub, faInstagram} from '@fortawesome/free-brands-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {faEnvelope} from '@fortawesome/free-solid-svg-icons'

library.add(faGithub, faInstagram, faLinkedin, faEnvelope)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(BootstrapVue);

Vue.config.productionTip = false

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
