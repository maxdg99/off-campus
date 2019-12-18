<template>
  <div class="home">
    <div class="uk-container uk-text-center">
      <h2>Welcome to Off Campus!</h2>
      <p>Searching for off campus housing doesn't have to be difficult. That's why we made this website: to make finding housing easier for students like you. We aggregate data from multiple property companies and allow you to search and sort that property data. Say goodbye to endlessly scrolling through property company websites.</p>
      <router-link to="/search" tag="button" class="uk-button uk-button-primary">Search Properties</router-link>
    </div>
    <br>
  </div>
</template>

<script>
export default {
  name: "home"
};
</script>
