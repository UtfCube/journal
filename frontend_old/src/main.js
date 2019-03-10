import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import store from './store'

axios.defaults.baseURL = 'http://localhost:5000/api'

Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
