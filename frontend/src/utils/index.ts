import Vue from 'vue'

export const EventBus = new Vue()

export function isValidJwt (jwt: string) {
  //if (!jwt || jwt.split('.').length < 3) {
  //  return false
  //}
  return true;
  const data = JSON.parse(atob(jwt.split('.')[1]))
  const exp = new Date(data.exp * 1000) // JS deals with dates in milliseconds since epoch
  const now = new Date()
  return now < exp
}