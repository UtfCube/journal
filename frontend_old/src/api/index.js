import axios from 'axios'

export default {
    getTutorHome(jwt) {
        return axios.get('/tutor/home', {headers: { Authorization: `Bearer: ${jwt}`}})
    },
    getStudentHome(jwt) {
        return axios.get('/student/home', {headers: { Authorization: `Bearer: ${jwt}`}})
    },
    authenticate (userData) {  
        return axios.post('/login', userData)
    },
    register (type, userData) {  
        return axios.post(`/register/${type}`, userData)
    }
}