import Vue from 'vue'  
import Vuex from 'vuex'

// imports of AJAX functions will go here
import Api from '@/api'  
import { isValidJwt, EventBus } from '@/utils'

Vue.use(Vuex)

const state = {  
  // single source of data
  userData: {},
  jwt: ''
}

const actions = {  
    // asynchronous operations
  
    //
    // omitting the other action methods...
    //
  
    login (context, userData) {
      return Api.authenticate(userData)
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
      return Api.register(payload.type, payload.form)
        .then(context.dispatch('login', userData))
        .catch(error => {
          console.log('Error Registering: ', error)
          EventBus.$emit('failedRegistering: ', error)
        })
    },
    async getStudentHome (context) {
      try { 
        const response = Api.getStudentHome(context.state.jwt.token)
        context.commit('setStudentInfo', { studentInfo: response.data })
        return null
      } catch (error) {
        return error;
      }
    },
    async getTutorHome (context) {
      try {
        const response = Api.getTutorHome(context.state.jwt.token);
        context.commit('setTutorInfo', { tutorInfo: response.data })
        return null;
      } catch (error) {
        return error;
      }
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
    },
    setTutorInfo (state, payload) {
      state.userData.info = payload.tutorInfo;
    },
    setStudentInfo (state, payload) {
      state.userData.info = payload.studentInfo;
    }
}

const getters = {  
    // reusable data accessors
    isAuthenticated (state) {
      return isValidJwt(state.jwt.token)
    },
    columns (state) {
      return state.userData.info[0].keys();
    }
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
  })
  
  export default store