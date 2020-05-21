<template>
  <div id="app">
    <nav class="uk-navbar-container uk-margin-bottom" uk-navbar>
      <div class="uk-navbar-left">
        <router-link to="/" class="uk-navbar-item uk-logo">Off Campus</router-link>
        <ul class="uk-navbar-nav uk-visible@s">
          <li>
            <router-link to="/">Home</router-link>
          </li>
          <li>
            <router-link to="/search" >Search</router-link>
          </li>
        </ul>
      </div>
      <div class="uk-navbar-right">
        <div class="uk-navbar-item">
          <a
            class="uk-navbar-toggle uk-hidden@s"
            uk-toggle="target: #mobile-sidebar"
            uk-navbar-toggle-icon
          ></a>
          <span v-show="!$root.isSignedIn"><button id="sign-up" uk-toggle="target: #sign-up-modal" class="uk-button uk-button-link">Sign Up</button> &nbsp; / &nbsp; <button id="sign-in" uk-toggle="target: #sign-in-modal" class="uk-button uk-button-link">Sign In</button></span>
          <div id='sign-up-modal' uk-modal>
            <div class="uk-modal-dialog uk-modal-body">
              <button class="uk-modal-close-default" type="button" uk-close></button>
              <h2 class="uk-modal-title">Sign Up</h2>
              <form class="uk-form-stacked">
                <div class="uk-margin">
                  <label class="uk-form-label" for="email">Email</label>
                  <input id="email" type="email" class="uk-input">
                </div>
                <div class="uk-margin">
                  <label class="uk-form-label" for="password">Password</label>
                  <input id="password" type="password" class="uk-input">
                </div>
                <div class="uk-margin">
                  <label class="uk-form-label" for="verify-password">Re-Type Password</label>
                  <input id="verify-password" type="password" class="uk-input">
                </div>
                <div class="google-sign-in-parent">
                  <button type="button" class="uk-button uk-button-primary">Sign Up</button>
                </div>
              </form>
              <div class="google-sign-in-parent uk-margin">
                or
              </div>
              <div class="google-sign-in-parent">
                <GoogleLogin :params="params" :renderParams="renderParams" :onSuccess="onSuccess" :onFailure="onFailure"></GoogleLogin>
              </div>
            </div>
          </div>
          <div id='sign-in-modal' uk-modal>
            <div class="uk-modal-dialog uk-modal-body">
              <button class="uk-modal-close-default" type="button" uk-close></button>
              <h2 class="uk-modal-title">Sign In</h2>
              <form class="uk-form-stacked">
                <div class="uk-margin">
                  <label class="uk-form-label" for="user-name">Email</label>
                  <input id="user-name" type="email" class="uk-input">
                </div>
                <div class="uk-margin">
                  <label class="uk-form-label" for="password">Password</label>
                  <input id="password" type="password" class="uk-input">
                </div>
                <div class="google-sign-in-parent">
                  <button type="button" class="uk-button uk-button-primary">Sign In</button>
                </div>
              </form>
              <div class="google-sign-in-parent uk-margin">
                or
              </div>
              <div class="google-sign-in-parent">
                <GoogleLogin :params="params" :renderParams="renderParams" :onSuccess="onSuccess" :onFailure="onFailure"></GoogleLogin>
              </div>
            </div>
          </div>
          <button v-show="$root.isSignedIn" class="uk-button uk-button-danger" v-on:click="logOut">Sign Out</button>
        </div>
      </div>
    </nav>

    <div id="mobile-sidebar" uk-offcanvas="overlay: true; flip: true">
      <div class="uk-offcanvas-bar">
        <button class="uk-offcanvas-close" type="button" uk-close></button>

        <ul class="uk-navbar-nav uk-flex uk-flex-column">
          <li class="uk-nav-header">Navigation</li>
          <li>
            <router-link to="/" uk-toggle="target: #mobile-sidebar">Home</router-link>
          </li>
          <li>
            <router-link to="/search" uk-toggle="target: #mobile-sidebar">Search</router-link>
          </li>
          <li>
            <!-- TODO: implement login with Google -->
            <a>Log In</a>
          </li>
        </ul>
      </div>
    </div>

    <router-view />
  </div>
</template>

<style lang="less">
@import "../node_modules/uikit/src/less/uikit.less";
@import "../node_modules/uikit/src/less/uikit.theme.less";
@offcanvas-bar-background: #fff;
@offcanvas-bar-color-mode: dark;

/* Sticky footer */
html {
  height: 100%;
}
body {
  min-height: 100%;
  display: grid;
  grid-template-rows: 1fr auto;
}
.google-sign-in-parent {
  display: flex;
  justify-content: center;
  align-items: center;
}
footer {
  grid-row-start: 2;
  grid-row-end: 3;
  padding-bottom: 0.5rem;
}
</style>

<script>
import UIkit from "uikit";
import Icons from "uikit/dist/js/uikit-icons";
import GoogleLogin from 'vue-google-login';
import Vue from 'vue'
import { LoaderPlugin } from 'vue-google-login';

Vue.use(LoaderPlugin, {
  client_id: "958584611085-255aprn4g9hietf5198mtkkuqhpov49q.apps.googleusercontent.com"
});

UIkit.use(Icons);

export default {
  name: "App",
  data() {
    return {
      params: {
          client_id: "958584611085-255aprn4g9hietf5198mtkkuqhpov49q.apps.googleusercontent.com"
      },
      renderParams: {
          width: 200,
          height: 40,
          longtitle: true
      }    }
  },
  components: {
      GoogleLogin
  },
  methods:{
    onSuccess: function(googleUser) {
      $.ajax({
        type: 'POST',
        url: 'http://localhost:8000/signIn',
        data:{
          id_token: googleUser.getAuthResponse().id_token
        },
        xhrFields: {
            withCredentials: true
        },
        crossDomain: true,
        success: response => {
          console.log('User successfully signed in.')
          Vue.GoogleAuth.then(auth2 => {
            auth2.signOut()
          })
          this.$root.isSignedIn = true
          UIkit.modal("#sign-in-modal").hide()
          UIkit.modal("#sign-up-modal").hide()
        },
        failure: () => {
          console.log('Failure logging in.')
        }
      })
    },
    onFailure: function(error){
      console.log(error)
    },
    logOut: function(){
      $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/signOut',
        xhrFields: {
          withCredentials: true
        },
        success: response => {
          console.log('User successfully signed out.')
          this.$root.isSignedIn = false      
        }
      })
    },
    isSignedIn: function(){
      $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/isSignedIn',
        xhrFields: {
          withCredentials: true
        },
        success: response => {
          console.log(response)
          this.$root.isSignedIn = response.isSignedIn      
        }
      })
    }
  },
  mounted: function() {
    this.isSignedIn()
  }
};

</script>


