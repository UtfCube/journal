import axios from 'axios'

export function getStudentHome(jwt) {
    return axios.get('/student/home', {headers: { Authorization: `Bearer: ${jwt}`}})
}

export function authenticate (userData) {  
    return axios.post('/login', userData)
}
  
export function register (type, userData) {  
    return axios.post(`/register/${type}`, userData)
}