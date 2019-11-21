<template>
  <div id="app">
    <nav class="uk-navbar-container uk-margin" uk-navbar>
      <div class="uk-navbar-left">
        <router-link to="/" class="uk-navbar-item uk-logo">Off Campus</router-link>
        <ul class="uk-navbar-nav">
          <li>
            <router-link to="/search">Search</router-link>
          </li>
        </ul>
      </div>
      <div class="uk-navbar-right">
        <div class="uk-navbar-item">
          <form>
            <button class="uk-button uk-button-default">Log In</button>
          </form>
        </div>
      </div>
    </nav>
    <router-view />
    <footer class="uk-text-center">&copy; 2019 Max Gruber, Andrew Haberlandt, Adam Lis</footer>
  </div>
</template>

<style lang="less">
@import "../node_modules/uikit/src/less/uikit.less";
@import "../node_modules/uikit/src/less/uikit.less";
</style>

<script>
import UIkit from "uikit";
import Icons from "uikit/dist/js/uikit-icons";
UIkit.use(Icons);
export default {
  name: "App"
};
</script>
