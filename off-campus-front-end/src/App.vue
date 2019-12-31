<template>
  <div id="app">
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
#navbar{
  background-color:white;
}
</style>

<script>
import UIkit from "uikit";
import Icons from "uikit/dist/js/uikit-icons";
import GoogleLogin from 'vue-google-login';
import Vue from 'vue'
import { LoaderPlugin } from 'vue-google-login';

UIkit.use(Icons);

export default {
  name: "App"
};
</script>


