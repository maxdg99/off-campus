<template>
  <div class="uk-background-cover" id="content">
    <div class="uk-container uk-text-center">
      <div id="button-text-group" class="uk-position-center">
        <h2 class="welcome-text">Go Bucks, Home Searching Sucks!</h2>
        <h3 class="welcome-text">Make finding a place easier, with Off Campus</h3>
        <router-link to="/search" tag="button" class="uk-button uk-button-primary">Search Properties</router-link>
      </div>
    </div>
    <footer id="footer" class="uk-text-center">&copy; {{new Date().getFullYear()}} Max Gruber, Andrew Haberlandt, Adam Lis</footer>
  </div>
</template>

<style scoped>
#content {
  background-image: 
    linear-gradient(
      rgba(0, 0, 0, 0.5),
      rgba(0, 0, 0, 0.5)
    ), 
    url(landing_page.jpg);
  height: calc(100vh - 82px);
  position: relative;
}

.welcome-text {
  color: white;
  font-weight: 600;
  margin: 10px;
}

#button-text-group {
  position: absolute;
  top: 30%;
}

#footer {
  color: white;
  position: absolute;
  bottom: 0%;
  width: 100%;
}
</style>

<script>
export default {
  name: "home"
};
</script>
