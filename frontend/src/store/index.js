import Vue from 'vue'  
import Vuex from 'vuex'

// imports of AJAX functions will go here
import { getStudentHome, authenticate, register } from '@/api'  
import { isValidJwt, EventBus } from '@/utils'

Vue.use(Vuex)

const state = {  
  // single source of data
  surveys: [],
  currentSurvey: {},
  userData: {},
  jwt: ''
}

const actions = {  
    // asynchronous operations
  
    //
    // omitting the other action methods...
    //
  
    login (context, userData) {
      return authenticate(userData)
        .then(response => {
          let { token } = response.data
          context.commit('setJwtToken', { jwt: { token } })
          context.commit('setUserData', { userData: { ...userData, type: response.data.type }})
        })
        .catch(error => {
          console.log('Error Authenticating: ', error)
          EventBus.$emit('failedAuthentication', error)
        })
    },
    register (context, payload) {
      let { username, password } = payload.form
      let userData = { username, password }
      context.commit('setUserData', { userData })
      return register(payload.type, payload.form)
        .then(context.dispatch('login', userData))
        .catch(error => {
          console.log('Error Registering: ', error)
          EventBus.$emit('failedRegistering: ', error)
        })
    },
    getStudentHome (context) {
      return getStudentHome(context.state.jwt.token)
    }
}

const mutations = {  
    // isolated data mutations
  
    //
    // omitting the other mutation methods...
    //
  
    setUserData (state, payload) {
      console.log('setUserData payload = ', payload)
      state.userData = payload.userData
    },
    setJwtToken (state, payload) {
      console.log('setJwtToken payload = ', payload)
      localStorage.token = payload.jwt.token
      state.jwt = payload.jwt
    }
}

const getters = {  
    // reusable data accessors
    isAuthenticated (state) {
      return isValidJwt(state.jwt.token)
    }
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
  })
  
  export default store