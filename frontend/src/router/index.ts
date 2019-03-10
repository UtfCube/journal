import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'

const routerOptions = [
  { 
    path: '/', 
    component: 'HelloWorld' 
  }, { 
    path: '/login',
    name: 'login', 
    component: 'Login' 
  }, { 
    path: '/student/home',
    name: 'studentHome', 
    component: 'StudentHome',
    beforeEnter (to: any, from: any, next: any) {
      if (!store.getters.isAuthenticated) {
        next('/login')
      } else {
        next()
      }
    }
  }, { 
    path: '/tutor/home',
    name: 'tutorHome', 
    component: 'TutorHome',
    beforeEnter (to: any, from: any, next: any) {
      if (!store.getters.isAuthenticated) {
        next('/login')
      } else {
        next()
      }
    }
  }, {
    path: '/register',
    name: 'register',
    component: 'Register'
  }, {
    path: '/student/:subject',
    name: 'progress',
    props: true,
    component: 'Progress',
    beforeEnter (to: any, from: any, next: any) {
      if (!store.getters.isAuthenticated) {
        next('/login')
      } else {
        next()
      }
    }
  }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
  routes,
  mode: 'history'
})
