<template>
  <div class="uk-card uk-card-small uk-card-default uk-card-hover">
    <div class="uk-card-media-top">
      <img v-bind:src="listing.image" class="listing-image" uk-img/>
    </div>
    <div class="uk-card-body listing-body">
      <div class="price-info-container">
        <div v-if="listing.price" class="listing-price">${{ listing.price }}</div>
        <div v-else>N/A</div>
        <span class="listing-info-container">
            <div class="listing-info">{{ listing.miles_from_campus }} mi</div> |
            <div class="listing-info">{{ `${listing.beds} ${listing.beds==1 ? "bed" : "beds"}` }}</div> |
            <div class="listing-info">{{ `${listing.baths} ${listing.baths==1 ? "bath" : "baths"}` }}</div>
        </span>
      </div>
      <div class="listing-address-parent">
        <a v-bind:href="listing.url" target="_blank" class="listing-address">{{ listing.pretty_address }}</a>
      </div>
      <div class="listing-availability-parent">
        <div class="listing-availability" v-if="listing.availability_mode=='Season'">Available this {{getMonth(listing.availability_date.month)}}</div>
        <div class="listing-availability" v-else-if="listing.availability_mode=='Month'">Available in {{this.months[listing.availability_date.month - 1]}}</div>
        <div class="listing-availability" v-else-if="listing.availability_mode=='Now'">Available Now</div>
        <div class="listing-availability" v-else-if="listing.availability_mode=='Date'">Available on {{getDate(listing.availability_date)}}</div>
      </div>
      <div class="listing-info-row">
        <a :class="{'liked': isLiked}" uk-icon="icon: heart; ratio: 2" @click="toggleLikedProperty()"></a>
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

.switcher {
  position: absolute;
  left: 0;
  top: 0;
}

.listing-body {
  padding: 5px;
}


.listing-image {
  height: 300px;
  width: 100%;
}

.listing-address-parent {
  margin-bottom: var(--card-section-margin);
}

.listing-address,
.listing-address:hover {
  display: inline-block;
  color: black;
  font-size: 1em;
  font-weight: 600;
}

.price-info-container {
  overflow: auto;
  margin-bottom: var(--card-section-margin);
}

.listing-info {
  display: inline;
  font-size: 1em;
  font-weight: 600;
  color: black;
}

.listing-info-container {
  float: right;
  line-height: 1.75em;
  vertical-align: middle;
}

.listing-price {
  float:left;
  font-weight: 600;
  font-size: 1.75em;
  color: black;
}

.listing-availability {
  font-size: 1em;
  font-weight: 600;
  color: black;
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
  data: function () {
    return {
      months: ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    }
  },
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
    },
    getDate(date) {
      var split_date = date.split("-")
      return `${split_date[1]}/${split_date[2]}/${split_date[0]}`
    },
    getMonth(date) {
      var split_date = date.split("-")
      if(split_date[1] == 1) {
        return "Winter"
      } else if(split_date[1] == 3) {
        return "Spring"
      } else if(split_date[1] == 6) {
        return "Summer"
      } else if(split_date[1] == 9) {
        return "Fall"
      }
    }
  }
};
</script>
