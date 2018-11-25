<template class="container-fluid">
    <div>
        <div class="loginForm">
            <div>
                <br/>
                <label>email</label><input class="form-control" type="email" name="email" v-model="email">
                <br/>
                <label>password</label><input class="form-control" type="password" name="password" v-model="password">
                <br/>
            </div>
        </div>
        <div class="loginButtonDiv">
            <button class="btn btn-success sharp loginButton" v-on:click="Login()">Login</button>
        </div>
    </div>
</template>

<script>
import {SendGetRequest, SendPostRequest, SetUserToken} from '../services/Rest'

export default {
  name: 'Login',
  props:{
      isLoggedIn:{
          default:false,
          type: Boolean
      }
  },
  data: function(){
      return {
          email: "",
          password: ""
      }
  },
  methods:{
      Login: function () {
          let vueContext = this
          SendPostRequest('/authenticate', {'email':this.email, 'password':this.password})
          .then(function(response){
              let token = response.body
              if (token)
              {
                vueContext.$parent.isLoggedIn = true;
                vueContext.$parent.UserToken = token;
                SetUserToken(token);
                vueContext.$parent.ChangeState(vueContext.$parent.viewStates.expenses)
              }
              else
              {
                  //vueContext.$emit("userLoginError", response.body)
              }
          }).catch(function (response){
              console.log(response)
          });
      }
  }
}
</script>

<style scoped>

@import "../index.css";

.loginButtonDiv{
    text-align: center;
    width: 50%;
    margin: 0 auto;
}
.loginButtonDiv button{
    width: 30vw;
    margin-top: 5vh;
    display: inline-block;
}
.loginForm{
    text-align: center;
    width: 50%;
    margin: 0 auto;
}
label{
    float:left;
}
</style>