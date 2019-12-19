<template>
  <div id="app">
    <nav class="uk-navbar-container uk-margin" uk-navbar>
      <div class="uk-navbar-left">
        <router-link to="/" class="uk-navbar-item uk-logo">Off Campus</router-link>
        <ul class="uk-navbar-nav uk-visible@s">
          <li>
            <router-link to="/">Home</router-link>
          </li>
          <li>
            <router-link to="/search">Search</router-link>
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
          <form class="uk-visible@s">
            <button id="sign-in-button" class="uk-button uk-button-default">{{userSignedIn ? "Sign Out" : "Sign In"}}</button>
          </form>
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

    <footer class="uk-text-center">&copy; 2019 Max Gruber, Andrew Haberlandt, Adam Lis</footer>
  </div>
</template>

<style lang="less">
@import "../node_modules/uikit/src/less/uikit.less";
@import "../node_modules/uikit/src/less/uikit.theme.less";
@offcanvas-bar-background: #fff;
@offcanvas-bar-color-mode: dark;
</style>

<script>
import UIkit from "uikit";
import Icons from "uikit/dist/js/uikit-icons";
UIkit.use(Icons);
export default {
  name: "App"
};
</script>
