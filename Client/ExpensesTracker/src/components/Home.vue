<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-light" style="background-color:">
        <a class="navbar-brand" v-on:click="ChangeState(viewStates.home)">Expenses Tracker</a>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
                <li v-for="tab in tabs" v-bind:key="tab.name">
                    <a class="nav-link" v-on:click="ChangeState(tab.stateName)" v-bind:class="{active: state == tab.stateName}" >{{tab.name}}</a>
                </li>
            </ul>
            <ul class="navbar-nav">
                <li class="nav-item" v-if="!isLoggedIn" v-on:click="ChangeState(viewStates.login)" v-bind:class="{active: state == 'login'}">
                    <a class="nav-link">Login</a>
                </li>
                <li class="nav-item" v-if="!isLoggedIn" v-on:click="ChangeState(viewStates.signup)" v-bind:class="{active: state == 'signup'}">
                    <a class="nav-link">Signup</a>
                </li>
                <li class="nav-item" v-if="isLoggedIn">
                    <a class="nav-link">Account</a>
                </li>
                <li class="nav-item" v-if="isLoggedIn" v-on:click="Logout">
                    <a class="nav-link">Logout</a>
                </li>
            </ul>
        </div>
        </nav>

        <div style="text-align:center" v-if="state == viewStates.home">
            <h1>Welcome to Expenses tracker</h1>
        </div>
        
        <Login v-if="state == viewStates.login"></Login>
        <UserExpenses v-if="state == viewStates.expenses"></UserExpenses>
        <Signup v-if="state == viewStates.signup"></Signup>


  </div>
</template>
<script>

import Login from './Login'
import UserExpenses from './UserExpenses'
import Signup from './Signup'
import { SetUserToken } from '../services/Rest';

export default {
  name: 'Home',
  components: {
      Login,
      Signup,
      UserExpenses
  },
  data:function () { 
    return {
        isLoggedIn:{
            type: Boolean,
            default: false
        },
        state: {
            type: String,
            default: "Login"
        },
        viewStates: {
            login: "login",
            home: "home",
            about: "about",
            signup: "signup",
            expenses: "expenses"
        },
        UserToken: {
            type: String,
            default: ""
        },
        tabs: [
            { stateName: 'home', name: "Home"}, 
            { stateName: 'about', name: "About"}, 
            { stateName: 'expenses', name: "Expenses"}
        ],
    }
  },
  methods:{
      Logout: function () {
          this.isLoggedIn = false
          this.UserToken = "";
          SetUserToken("");
      },

      ChangeState: function(newState) {
          this.state = newState;
      },
  },
  created:function(){
      this.state = this.viewStates.home;
      this.isLoggedIn = false;
  }

}
</script>

<style scoped>

</style>


