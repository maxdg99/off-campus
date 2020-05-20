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
            <button id="sign-in-button" class="uk-button uk-button-default">Sign In</button>
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
            <a>Sign In</a>
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
  grid-template-rows: auto 1fr auto;
}
footer {
  grid-row-start: 3;
  grid-row-end: 4;
  padding: 0.5rem 0;
}
</style>

<script>
import UIkit from "uikit";
import Icons from "uikit/dist/js/uikit-icons";
UIkit.use(Icons);
export default {
  name: "App"
};
</script>
