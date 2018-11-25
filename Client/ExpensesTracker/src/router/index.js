import Vue from 'vue'
import Router from 'vue-router'
import UserExpenses from '../components/UserExpenses'
import Login from '../components/Login'

Vue.use(Router)

export default new Router({
   routes: [
    {path: '/expenses', component: UserExpenses},
    {path: '/login', component: Login}
  ]
})
