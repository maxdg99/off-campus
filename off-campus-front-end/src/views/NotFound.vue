<template>
  <div class="not-found">
    <div class="uk-container uk-text-center">
      <h1>Page Not Found</h1>
      <div class="uk-grid-medium uk-flex-center" uk-grid>
        <div>
          <router-link to="/" tag="button" class="uk-button uk-button-primary">Home</router-link>
        </div>
        <div>
          <router-link to="/search" tag="button" class="uk-button uk-button-primary">Search</router-link>
        </div>
      </div>
    </div>
    <br />
  </div>
</template>

<script>
export default {
  name: "not-found"
};
</script>
