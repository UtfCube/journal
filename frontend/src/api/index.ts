import axios from 'axios'

export default class Api {
    public static getTutorHome(jwt: string) {
        return axios.get('/tutor/home', { headers: { Authorization: `Bearer: ${jwt}`}})
    }
    public static getStudentHome(jwt: string) {
        return axios.get('/student/home', { headers: { Authorization: `Bearer: ${jwt}`}})
    }
    public static addNewSubject(jwt: string, info: object) {
        return axios.post('/tutor/home', info, { headers: { Authorization: `Bearer: ${jwt}`}})
    }
    public static authenticate (userData: any) {  
        return axios.post('/login', userData)
    }
    public static register (type: string, userData: any) {  
        return axios.post(`/register/${type}`, userData)
    }
    public static getCheckPoints(jwt: string, params: any) {
        return axios.get(`/tutor/${params.subject_name}/${params.group_id}`, { headers: { Authorization: `Bearer: ${jwt}`}})
    }
    public static addCheckPoint(jwt: string, payload: any) {
        return axios.post(`/tutor/${payload.subject_name}/${payload.group_id}`, 
            payload.checkpoint,
            { headers: { Authorization: `Bearer: ${jwt}`}});
    }
    public static getProgress(jwt: string, subject: any) {
        return axios.get(`/student/${subject}`, { headers: { Authorization: `Bearer: ${jwt}`}});
    }
}