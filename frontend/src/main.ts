import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';
import Buefy from 'buefy'

Vue.use(Buefy)

Vue.config.productionTip = false;
axios.defaults.baseURL = process.env.VUE_APP_SERVER_HOST
console.log(process.env.VUE_APP_SERVER_HOST)

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
