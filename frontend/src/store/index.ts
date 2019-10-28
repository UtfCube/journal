import Vue from 'vue'  
import Vuex from 'vuex'

// imports of AJAX functions will go here
import Api from '@/api'  
import { isValidJwt, getAccessToken } from '@/utils'

Vue.use(Vuex)

const state = {  
  // single source of data
  associations: [],
  groups: [],
  subjects: [],
  access_token: "",
  userData: {},
  gradesTable: [],
  currentCheckpoints: [],
  progress: {},
  tutors: [],
  adminInfo: {}
}

const actions = {  
    // asynchronous operations
  
    //
    // omitting the other action methods...
    //
    async login (context: any, userData: any) {
      try {
        const response = await Api.authenticate(userData);
        const { access_token, role } = response.data
        context.commit('setJwtToken', { jwt: access_token })
        context.commit('setUserData', { userData: {...userData, role}})
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
        await Api.register(payload);
        return await context.dispatch('login', userData);
      }
      catch (error) {
        return error.response.data.msg
      }
    },
    async logout (context: any) {
      try {
        await Api.logout(context.state.access_token);
        context.commit('deleteJwtToken');
        return null;
      }
      catch (error) {
        return error.response.data.msg;
      }
    },
    async changePassword (context: any, payload: any) {
      try { 
        await Api.changePassword(context.state.access_token, payload)
        return null
      } catch (error) {
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
    async getUsers(context: any) { 
      try { 
        const response = await Api.getUsers(context.state.access_token)
        context.commit('setAdminInfo', { info: response.data })
        return null
      } catch (error) {
        return error.response.data.msg;
      }
    },
    async getTutorHome(context: any) {
      try {
        let response = await Api.getTutorHome(context.state.access_token)
        context.commit('setAssociations', { associations: response.data });
        response = await Api.getGroups(context.state.access_token)
        context.commit('setGroups', { groups: response.data });
        response = await Api.getSubjects(context.state.access_token)
        context.commit('setSubjects', { subjects: response.data });
        return null;
      }
      catch (error) {
        return error.response.data.msg;
      }
    },
    async getCheckpoints(context: any, payload: any) {
      try {
        const response = await Api.getCheckpoints(context.state.access_token, payload);
        context.commit('setCurrentCheckpoints', {checkpoints: response.data});
        return null;
      }
      catch (error) {
        return error.response.data.msg;
      }
    },
    async getGradesTable(context: any, payload: any) {
      try {
        const response = await Api.getGradesTable(context.state.access_token, payload);
        context.commit('setGradesTable', { gradesTable: response.data });
      }
      catch (error) {
        return error.response.data.msg;
      }
    },
    async getTutors(context: any, payload: any) {
      try {
        const response = await Api.getTutors(context.state.access_token);
        context.commit('setTutors', { tutors: response.data });
      }
      catch (error) {
        return error.response.data.msg;
      }
    },
    async generatePassword(context: any, payload: any) {
      try {
        const response = await Api.generatePassword(context.state.access_token, payload);
        const {password} = response.data
        context.commit('setNewPassword', { ...payload, password: password })
        return null;
      }
      catch (error) {
        return error.response.data.msg;
      }
    },
    async updateGradesTable(context: any, payload: any) {
      try {
        await Api.updateGradesTable(context.state.access_token, payload);
        context.commit('updateGradesTable', { newProgress: payload.newProgress })
        return null;
      }
      catch (error) {
        return error.response.data.msg;
      }
    },
    async addAssociation (context: any, payload: any) {
      try {
        await Api.addAssociation(context.state.access_token, payload);
        context.commit('updateTutorInfo', { newInfo: payload });
        return null;
      } 
      catch (error) {
        return error.response.data.msg;
      }
    },
    async addDates (context: any, payload: any) {
      try {
        await Api.addDates(context.state.access_token, payload);
        context.commit('updateDates', { newDates: payload.dates });
      } catch (error) {
        return error.response.data.msg;
      }
    },
    async addProgress (context: any, payload: any) { 
      try {
        await Api.addProgress(context.state.access_token, payload);
        context.commit('updateGradesTable', { newProgress: payload.progress });
      } catch (error) {
        console.log(error)
        return error.response.data.msg;
      }
    },
    async AdminUpload (context: any, payload: any) {
      try {
        const response = await Api.AdminUpload(context.state.access_token, payload);
        context.commit('setAdminInfo', { info: response.data });
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
      localStorage.setItem('access_token', payload.jwt)
      //localStorage.access_token = payload.jwt
    },
    setTutorInfo (state: any, payload: any) {
      console.log('setTutorInfo payload = ', payload);
      Vue.set(state.userData, 'info', payload.tutorInfo)
    },
    setAssociations(state: any, payload: any) {
      console.log('setAssociations payload = ', payload)
      //state.associations = payload.associations
      Vue.set(state.userData, 'info', payload.associations)
    },
    setGroups (state: any, payload: any) {
      console.log('setGroups payload = ', payload)
      state.groups = payload.groups
    },
    setSubjects (state: any, payload: any) {
      console.log('setSubjects payload = ', payload)
      state.subjects = payload.subjects
    },
    setTutors (state: any, payload: any) {
      console.log('setTutors payload = ', payload)
      state.tutors = payload.tutors
    },
    setAdminInfo (state: any, payload: any) {
      console.log('setAdminInfo payload = ', payload)
      state.adminInfo = payload.info
    },
    setNewPassword (state: any, payload: any) {
      console.log('setNewPassword payload = ', payload)
      let index = state.adminInfo.tutors.findIndex((x:any) => x.username === payload.username)
      if (index === -1) {
        index = state.adminInfo.students.findIndex((x:any) => x.username === payload.username)
        console.log(index)
        Vue.set(state.adminInfo.students, index, {...state.adminInfo.students, ...payload})
      } else {
        console.log(index)
        Vue.set(state.adminInfo.tutors, index, {...state.adminInfo.students, ...payload})
      }
    },
    updateProgress(state: any, payload: any) {
      console.log("update progress", payload)
      Vue.set(payload.progress, payload.property, payload.value);
    },
    sortGradeTable(state:any, payload:any) {
      console.log("sort grade table ", payload)
      let cp_name = payload.cp_name
      let sortGrades = JSON.parse(JSON.stringify(state.gradesTable))
      let compare = (a:any, b:any) => {
        let a_cp_progress = a.progress.find((x:any) => x.name == cp_name)
        let b_cp_progress =  b.progress.find((x:any) => x.name == cp_name)
        if (a_cp_progress) {
          if (b_cp_progress) {
            let a_cp_f_progress = a_cp_progress.results.find((x:any) => x.name == 'Оценка')
            let b_cp_f_progress = b_cp_progress.results.find((x:any) => x.name == 'Оценка')
            if (a_cp_f_progress) {
              if (b_cp_f_progress) {
                if ( a_cp_f_progress.result < b_cp_f_progress.result ){
                  return 1;
                }
                if ( a_cp_f_progress.result > b_cp_f_progress.result ){
                  return -1;
                }
                return 0;
              }
              else {
                return -1;
              } 
            }
            else {
              if (b_cp_f_progress) {
                  return 1;
                }
              else {
                return 0;
              }
            }
          }
          else {
            let a_cp_f_progress = a_cp_progress.results.find((x:any) => x.name == 'Оценка')
            if (a_cp_f_progress) {
              return -1;
            }
            else {
              return 0;
            }
          }
        }
        else {
          if (b_cp_progress) {
            let b_cp_f_progress = b_cp_progress.results.find((x:any) => x.name == 'Оценка')
            if (b_cp_f_progress) {
              return 1;
            }
            else {
              return 0;
            }
          }
          else {
            return 0;
          }
        }
      }
      sortGrades.sort(compare)
      state.gradesTable = sortGrades
    },
    updateGradesTable(state: any, payload: any) {
      console.log("updateGradesTable payload = ", payload)
      for (let newInfo of payload.newProgress) {
        let userInfo = state.gradesTable.find((x: any) => x.username == newInfo.username)
        for (let progress of newInfo.progress) {
          let userProgress = userInfo.progress.find((x: any) => x.name == progress.name)
          if (userProgress) {
            for (let result of progress.results) {
              let userResult = userProgress.results.find((x: any) => x.name == result.name)
              if (userResult) {
                Vue.set(userResult, 'result', result.result)
              }
              else {
                Vue.set(userProgress.results, userProgress.results.length, result)
              }
            }
          }
          else {
            Vue.set(userInfo.progress, userInfo.progress.length, progress)
          }
        }
      }
    },
    updateDates(state:any, payload: any) {
      console.log('updateDates payload = ', payload);
      for (let checkpoint in payload.newDates) {
        let cp = state.currentCheckpoints.find((x: any) => x.name == checkpoint)
        let new_dates = [...cp.dates]
        for (let date_info of payload.newDates[checkpoint]) {
          let i = new_dates.findIndex((x: any) => x.name == date_info.name)
          new_dates[i] = date_info 
        }
        Vue.set(cp, 'dates', new_dates)
      }
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
    setGradesTable(state: any, payload: any) {
      console.log('setGradesTable payload = ', payload);
      state.gradesTable = payload.gradesTable;
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

    getFields(state: any) {
      let fields = []
      for (let checkpoint of state.currentCheckpoints) {
        let tmp = JSON.parse(JSON.stringify(checkpoint.fields))
        tmp.forEach((el: any) => el['cp_name'] = checkpoint.name)
        fields.push(...tmp)
      }
      return fields
    },
    getUsername(state: any) {
      return state.userData.username;
    },
    getProgress (state: any, getters: any) {
      let newProgress = JSON.parse(JSON.stringify(state.gradesTable))
      for (let userInfo of newProgress) {
        let old_progress = userInfo.progress
        let fields = []
        for (let checkpoint of state.currentCheckpoints) {
          let tmp = JSON.parse(JSON.stringify(checkpoint.fields))
          tmp.forEach((el: any) => el['cp_name'] = checkpoint.name)
          fields.push(...tmp)
        }
        userInfo.progress = fields
        for (let checkpoint_res of old_progress) {
          for (let field_res of checkpoint_res.results) {
            let update_res = userInfo.progress.find((x:any) => x.cp_name == checkpoint_res.name && x.name == field_res.name)
            update_res['result'] = field_res['result']
          }
        }
      }
      return newProgress
    },

    getProgressByCheckpoint: (state: any) => (checkpoint: string) => {
      let pr = state.gradesTable.filter((x: any) => !!x.progress[checkpoint]).map((x: any) => { 
        return {
          firstname: x.firstname,
          lastname: x.lastname,
          patronymic: x.patronymic,
          user_id: x.user_id,
          progress: x.progress[checkpoint]
        }
      });
      return pr;
    },
    getNewProgress(state: any) {
      return state.gradesTable.map((x: any) => {
        return {
          user_id: x.user_id,
          progress: {}
        }
      });
    }
}

const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters
  })
  
  export default store