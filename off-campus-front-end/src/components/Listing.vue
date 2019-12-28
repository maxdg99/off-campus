<template>
  <div class="uk-card uk-card-small uk-card-default uk-card-hover uk-card-body">
    <div class="listing-address-parent">
      <a v-bind:href="listing.url" target="_blank" class="listing-address">{{ listing.address }}</a>
    </div>
    <img v-bind:src="listing.image_url" class="listing-image" />
    <div class="listing-info-container">
      <div class="listing-info-row">
        <div v-if="listing.price" class="listing-info listing-price">${{ listing.price }}</div>
        <div v-if="!listing.price" class="listing-info">N/A</div>
        <div class="listing-info">{{ listing.miles_from_campus }} mi</div>
      </div>
      <div class="listing-info-row">
        <div class="listing-info">{{ listing.num_bedrooms }} beds</div>
        <div class="listing-info">{{ listing.num_bathrooms }} baths</div>
      </div>
      <div class="listing-info-row">
        <a :class="{liked: isLiked}" uk-icon="icon: heart; ratio: 2" @click="toggleLikedProperty()"></a>
      </div>
    </div>
  </div>
</template>

<style scoped>
:root {
  --card-section-margin: 10px;
}

.liked {
  color: rgb(247, 93, 177)
}

.listing-address-parent {
  text-align: center;
  margin-bottom: var(--card-section-margin);
}

.listing-address,
.listing-address:hover {
  display: inline-block;
  color: black;
  font-size: 1.125em;
}

.listing-image {
  display: block;
  margin: auto;
  height: 200px;
  margin-bottom: var(--card-section-margin);
}

.listing-info-container {
  display: block;
  margin-left: 20%;
  margin-right: 10%;
  font-size: 1.125em;
  color: black;
}

.listing-info-row {
  width: 100%;
}

.listing-info {
  display: inline-block;
  width: 50%;
}

.listing-price {
  font-weight: bold;
  color: green;
}
</style>

<script>
import GoogleLogin from 'vue-google-login';
import Vue from 'vue'
import { LoaderPlugin } from 'vue-google-login';

Vue.use(LoaderPlugin, {
  client_id: "958584611085-255aprn4g9hietf5198mtkkuqhpov49q.apps.googleusercontent.com"
});

export default {
  name: "Listing",
  props: {
    id: Number,
    listing: Object,
    isLiked: Boolean
  },
  methods:{
    toggleLikedProperty: function () {
      if(this.$root.isSignedIn) {
        $.ajax({
          type: 'GET',
          url: 'http://localhost:8000/toggleLikedProperty',
          data: {
            property_id: this.id
          },
          xhrFields: {
            withCredentials: true
          },
          success: (data) => {
            this.$emit('update-isLiked', data.isLiked)
            console.log("Listing successfully toggled to " + data.isLiked)
          },
          failure: (response) => {
            if(response.status == 401){
              console.log("Error: User is not signed in")
              this.$root.isSignedIn = false
            }
            else if(response.status == 404) {
              console.log("Error: Listing does not exists.")
            }
          }
        });
      }
      else {
        alert("There is no signed in user. Please sign in with google.")
      }
    }
  }
};
</script>
