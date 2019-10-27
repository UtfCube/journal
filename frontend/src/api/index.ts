import axios from 'axios'

export default class Api {
    public static getTutorHome(jwt: string) {
        return axios.get('/home', { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static addAssociation(jwt: string, info: object) {
        return axios.post('/associations', info, { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static addDates(jwt: string, payload: any) {
        return axios.post(`/${payload.subject_name}/${payload.group_id}/dates`, payload.dates, { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static addProgress(jwt: string, payload: any) {
        return axios.post(`/${payload.subject_name}/${payload.group_id}/progress`, payload.progress, { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static getTutors(jwt: string) {
        return axios.get('/tutors', { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static getGroups(jwt: string) {
        return axios.get('/groups', { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static getSubjects(jwt: string) {
        return axios.get('/subjects', { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static AdminUpload(jwt: string, formData: any) {
        return axios.post('/home', formData, { headers: { 
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${jwt}`
        }});
    }
    public static getStudentHome(jwt: string) {
        return axios.get('/home', { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static authenticate (userData: any) {  
        return axios.post('/login', userData)
    }
    public static register (userData: any) {  
        return axios.post(`/register`, userData)
    }
    public static getCheckpoints(jwt: string, params: any) {
        return axios.get(`/${params.subject_name}/checkpoints`, { headers: { Authorization: `Bearer ${jwt}`}})
    }
    public static addCheckpoints(jwt: string, payload: any) {
        return axios.post(`/tutor/${payload.subject_name}/${payload.group_id}/checkpoints`, 
            { checkpoints: payload.checkpoints },
            { headers: { Authorization: `Bearer ${jwt}`}});
    }
    public static getGradesTable(jwt: string, params: any) {
        return axios.get(`/${params.subject_name}/${params.group_id}/progress`,
            { headers: { Authorization: `Bearer ${jwt}`}});
    }
    public static updateGradesTable(jwt: string, payload: any) {
        return axios.post(`/tutor/${payload.subject_name}/${payload.group_id}`, 
            payload.newProgress,
            { headers: { Authorization: `Bearer ${jwt}`}});
    }
    public static getProgress(jwt: string, params: any) {
        return axios.get(`/tutor/${params.subject_name}/${params.group_id}/${params.checkpoint_name}`,
            { headers: { Authorization: `Bearer ${jwt}`}});
    }
    public static logout(jwt: string) {
        return axios.post('/logout/access', {}, { headers: { Authorization: `Bearer ${jwt}`}})
    }
}