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
  
    login (context: any, userData: any) {
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
    register (context: any, payload: any) {
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
    async getStudentHome (context: any) {
      try { 
        const response = await Api.getStudentHome(context.state.jwt.token)
        context.commit('setStudentInfo', { studentInfo: response.data })
        return null
      } catch (error) {
        return error;
      }
    },
    getTutorHome (context: any) {
      return Api.getTutorHome(context.state.jwt.token)
        .then(response => {
          context.commit('setTutorInfo', { tutorInfo: response.data })
        })
        
    },
    async addNewSubject (context: any, payload: any) {
      try {
        await Api.addNewSubject(context.state.jwt.token, payload);
        context.commit('updateTutorInfo', { newInfo: payload });
        return null;
      } catch(error) {
        return error;
      }
    }
}

const mutations = {  
    // isolated data mutations
  
    //
    // omitting the other mutation methods...
    //
  
    setUserData (state: any, payload: any) {
      console.log('setUserData payload = ', payload)
      state.userData = payload.userData
    },
    setJwtToken (state: any, payload: any) {
      console.log('setJwtToken payload = ', payload)
      localStorage.token = payload.jwt.token
      state.jwt = payload.jwt
    },
    setTutorInfo (state: any, payload: any) {
      console.log('setTutorInfo payload = ', payload);
      Vue.set(state.userData, 'info', payload.tutorInfo)
    },
    updateTutorInfo (state: any, payload: any) {
      Vue.set(state.userData, 'info', [...state.userData.info, payload.newInfo])
    },
    setStudentInfo (state: any, payload: any) {
      Vue.set(state.userData, 'info', payload.studentInfo);
    },
}

const getters = {  
    // reusable data accessors
    isAuthenticated (state: any) {
      return isValidJwt(state.jwt.token)
    },
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
  })
  
  export default store