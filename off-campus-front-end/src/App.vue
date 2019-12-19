<template>
  <div id="app">
    <nav class="uk-navbar-container" uk-navbar>
      <div class="uk-navbar-left">
        <router-link to="/" id="logo" class="uk-navbar-item uk-logo">Off Campus</router-link>
        <ul class="uk-navbar-nav uk-visible@s">
          <li>
            <router-link to="/">Home</router-link>
          </li>
          <li>
            <router-link to="/search" >Search</router-link>
          </li>
          <li v-if="$root.isSignedIn">
            <router-link to="/favorites">Favorites</router-link>
          </li>
          <li>
            <router-link to="/about">About</router-link>
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
          <GoogleLogin class="uk-visible@s" v-show="!$root.isSignedIn" :params="params" :renderParams="renderParams" :onSuccess="onSuccess" :onFailure="onFailure"></GoogleLogin>
          <button class="uk-button uk-button-danger uk-visible@s" v-on:click="logOut()" v-show="$root.isSignedIn">Sign Out</button>
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
            <router-link to="/about" uk-toggle="target: #mobile-sidebar">About Us</router-link>
          </li>
          <li>
            <GoogleLogin class="mobile-button" v-show="!$root.isSignedIn" :params="params" :renderParams="renderParams" :onSuccess="onSuccess" :onFailure="onFailure"></GoogleLogin>
            <button v-on:click="logOut()" v-show="$root.isSignedIn" class="uk-button uk-button-danger mobile-button">Sign Out</button>
          </li>
          <!-- <li>
            <a>Sign In</a>
          </li> -->
        </ul>
      </div>
    </div>

    <router-view />
  </div>
</template>

<style lang="scss">
@import "@/scss/_variables.scss";

/* UIKit variable overrides */
$offcanvas-bar-background: #f8f8f8;
$offcanvas-bar-color-mode: dark;
$button-primary-background: $primary-color;

/* UIKit import */
@import "uikit/src/scss/variables-theme.scss";
@import "uikit/src/scss/mixins-theme.scss";
@import "uikit/src/scss/uikit-theme.scss";

#logo{
  font-weight: 600;
}

.mobile-button {
  margin: 0;
  display: block;
  margin-left: auto;
  margin-right: auto;

  /* 
    Don't worry about this, the google sign in component is weird. 
    This is needed to center the button.
  */
  & > div {
    margin: 0;
    display: block;
    margin-left: auto;
    margin-right: auto;
  }
}

nav {
  border-bottom: $primary-color 0.125rem solid;
}

/* Sticky footer */
html {
  height: 100%;
}
body {
  min-height: 100%;
  display: grid;
  grid-template-rows: auto 1fr auto;
}

footer {
  grid-row-start: 3;
  grid-row-end: 4;
  padding: 0.5rem 0;
}

/* Smaller OpenStreetMap attribution */
.ol-attribution {
  font-size: 0.75rem;
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
      }    
    }
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


