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
            <router-link to="/search">Search</router-link>
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
          <!-- <form class="uk-visible@s">
            <button id="sign-in-button" class="uk-button uk-button-default">Sign In</button>
          </form> -->
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
            <!-- TODO: implement login with Google
            <a>Sign In</a> -->
          </li>
        </ul>
      </div>
    </div>

    <router-view />
  </div>
</template>

<style lang="scss">
$primary-color: hsl(200, 100%, 38%);

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
UIkit.use(Icons);
export default {
  name: "App"
};
</script>
