import Vue from 'vue'  
import Vuex from 'vuex'

// imports of AJAX functions will go here
import Api from '@/api'  
import { isValidJwt, EventBus } from '@/utils'

Vue.use(Vuex)

const state = {  
  // single source of data
  access_token: "",
  userData: {},
  currentCheckpoints: [],
  progress: [],
}

const actions = {  
    // asynchronous operations
  
    //
    // omitting the other action methods...
    //
    async login (context: any, userData: any) {
      try {
        const response = await Api.authenticate(userData);
        const { access_token } = response.data
        context.commit('setJwtToken', { jwt: access_token })
        context.commit('setUserData', { userData: userData})
        return null
      }
      catch (error) {
        return error.response.data.msg
      }
    },
    async register (context: any, payload: any) {
      try {
        let { username, password } = payload.form
        let userData = { username, password }
        context.commit('setUserData', { userData })
        await Api.register(payload.type, payload.form);
        return await context.dispatch('login', userData);
      }
      catch (error) {
        return error.response.data.msg
      }
    },
    async logout (context: any) {
      try {
        await Api.logout(state.access_token);
        context.commit('deleteJwtToken');
        return null;
      }
      catch (error) {
        return error.response.data.msg;
      }
    },
    async getStudentHome (context: any) {
      try { 
        const response = await Api.getStudentHome(context.state.access_token)
        context.commit('setStudentInfo', { studentInfo: response.data })
        return null
      } catch (error) {
        return error.response.data.msg;
      }
    },
    async getTutorHome(context: any) {
      try {
        const response = await Api.getTutorHome(context.state.access_token);
        context.commit('setTutorInfo', { tutorInfo: response.data });
        return null;
      }
      catch (error) {
        return error.response.data.msg;
      }
    },
    async getCheckpoints(context: any, payload: any) {
      try {
        const response = await Api.getCheckpoints(context.state.access_token, payload);
        context.commit('setCurrentCheckpoints', response.data);
        return null;
      }
      catch (error) {
        return error.response.data.msg;
      }
    },
    async addNewSubject (context: any, payload: any) {
      try {
        await Api.addNewSubject(context.state.access_token, payload);
        context.commit('updateTutorInfo', { newInfo: payload });
        return null;
      } 
      catch (error) {
        return error.response.data.msg;
      }
    },
    async addCheckpoints(context: any, payload: any) {
      try {
        await Api.addCheckpoints(context.state.access_token, payload);
        context.commit('updateCurrentCheckpoints', {checkpoints: payload.checkpoints});
      }
      catch (error) {
        return error.response.data.msg;
      }
    },
    async getProgress(context: any, payload: any) {
      try {
        const response = await Api.getProgress(context.state.access_token, payload);
        context.commit('setProgress', { progress: response.data, checkpoint: payload.checkpoint_name });
        return null;
      }
      catch (error) {
        return error.response.data.msg;
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
      state.access_token = payload.jwt;
      //localStorage.access_token = payload.jwt
    },
    setTutorInfo (state: any, payload: any) {
      console.log('setTutorInfo payload = ', payload);
      Vue.set(state.userData, 'info', payload.tutorInfo)
    },
    updateTutorInfo (state: any, payload: any) {
      Vue.set(state.userData, 'info', [...state.userData.info, payload.newInfo])
    },
    setStudentInfo (state: any, payload: any) {
      console.log('setStudentInfo payload = ', payload.studentInfo)
      Vue.set(state.userData, 'info', payload.studentInfo);
    },
    setCurrentCheckpoints(state: any, payload: any) {
      console.log('setCurrentCheckpoints payload = ', payload);
      state.currentCheckpoints = payload.checkpoints;
    },
    setProgress(state:any, payload: any) {
      console.log('setProgress payload = ', payload);
      Vue.set(state.progress, payload.checkpoint, payload.progress);
    },
    updateCurrentCheckpoints(state: any, payload: any) {
      state.currentCheckpoints = [...state.currentCheckpoints, ...payload.checkpoints]
    },
    deleteJwtToken (state: any, payload: any) {
      console.log('deleteJwtToken')
      state.access_token = "";
      //localStorage.access_token = '';
    }
}

const getters = {  
    // reusable data accessors
    isAuthenticated (state: any) {
      return isValidJwt(state.access_token);
    },
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
  })
  
  export default store