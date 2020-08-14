<template>
  <div class="uk-card uk-card-small uk-card-default uk-card-hover" :class="{inactive: !listing.active}">
    <div class="uk-card-media-top">
      <img v-bind:src="listing.image" class="listing-image" v-show="!showMap" uk-img />
      <div class="listing-map" v-show="showMap" ref="smolMap" />
      <a @click="isLiked ? unlikeProperty() : likeProperty()"  v-show="this.$root.isSignedIn" id="like-button">
        <svg viewBox="0 0 512 512">
          <path v-bind:fill="isLiked ? 'rgb(247, 93, 177)' : 'gray'" d="M376,30c-27.783,0-53.255,8.804-75.707,26.168c-21.525,16.647-35.856,37.85-44.293,53.268
            c-8.437-15.419-22.768-36.621-44.293-53.268C189.255,38.804,163.783,30,136,30C58.468,30,0,93.417,0,177.514
            c0,90.854,72.943,153.015,183.369,247.118c18.752,15.981,40.007,34.095,62.099,53.414C248.38,480.596,252.12,482,256,482
            s7.62-1.404,10.532-3.953c22.094-19.322,43.348-37.435,62.111-53.425C439.057,330.529,512,268.368,512,177.514
            C512,93.417,453.532,30,376,30z"/>
        </svg>
      </a>
    </div>
    <div class="uk-card-body listing-body">
      <div class="listing-price-and-info-container">
        <div v-if="listing.price" class="listing-price">${{ listing.price }}</div>
        <div v-else>N/A</div>
        <div>
          <span>{{ listing.miles_from_campus }} mi</span>
          <span>&nbsp;|&nbsp;</span>
          <span>{{ `${listing.beds} ${listing.beds==1 ? "bed" : "beds"}` }}</span>
          <span>&nbsp;|&nbsp;</span>
          <span>{{ `${listing.baths} ${listing.baths==1 ? "bath" : "baths"}` }}</span>
        </div>
      </div>
      <div class="listing-address-container">
        <a
          v-bind:href="listing.url"
          target="_blank"
          class="listing-address"
        >{{ listing.pretty_address }}</a>
      </div>
      <div>
        <div
          v-if="listing.availability_mode=='Season'"
        >Available this {{getMonth(listing.availability_date.month)}}</div>
        <div
          v-else-if="listing.availability_mode=='Month'"
        >Available in {{this.months[listing.availability_date.month - 1]}}</div>
        <div v-else-if="listing.availability_mode=='Now'">Available Now</div>
        <div
          v-else-if="listing.availability_mode=='Date'"
        >Available on {{getDate(listing.availability_date)}}</div>
      </div>
      <span v-if="!listing.active">This listing is no longer available.</span>
    </div>
    <div class="map-icon">
      <a uk-icon="location" v-on:click="toggleMap" v-show="canFlip"></a>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/scss/_variables.scss";

$card-section-margin: 0;
$listing-image-map-height: 200px;

#like-button {
  position: absolute;
  top: 0;
  right: 0;
  margin-top: 5px;
  margin-right: 5px;

  width: 30px;
  height: 30px;

  background-color: white;
  border-radius: 24px;
  padding: 8px;
}

.inactive {
  border: 2px orange solid;
}

.switcher {
  position: absolute;
  left: 0;
  top: 0;
}

.listing-body {
  padding: 5px 10px 10px 10px;
  font-weight: 600;
  color: black;
}

.listing-image {
  height: $listing-image-map-height;
  width: 100%;
  object-fit: cover;
}

.listing-map {
  height: $listing-image-map-height;
}

.listing-price-and-info-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $card-section-margin;
}

.listing-price {
  font-size: 1.75em;
}

.listing-address-container {
  margin-bottom: $card-section-margin;
}

.listing-address,
.listing-address:hover {
  display: inline-block;
  color: inherit;
}

.map-icon {
  position: absolute;
  right: 20px;
  bottom: 20px;

  @media screen and (min-width: $min-laptop-screen-width) {
    display: none;
  }
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
  data: function() {
    return {
      showMap: false,
      mapReady: false,
      months: [
        "January",
        "Febuary",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
      ]
    };
  },
  props: {
    id: Number,
    listing: Object,
    isLiked: Boolean,
    canFlip: {
      type: Boolean,
      default: true
    }
  },
  methods:{
    likeProperty: function () {
      if(this.$root.isSignedIn) {
        $.ajax({
          type: 'GET',
          url: 'http://localhost:8000/likeProperty',
          data: {
            property_id: this.id
          },
          xhrFields: {
            withCredentials: true
          },
          success: (data) => {
            this.$emit('update-isLiked', true)
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
    unlikeProperty: function () {
      if(this.$root.isSignedIn) {
        $.ajax({
          type: 'GET',
          url: 'http://localhost:8000/unlikeProperty',
          data: {
            property_id: this.id
          },
          xhrFields: {
            withCredentials: true
          },
          success: (data) => {
            this.$emit('update-isLiked', false)
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
    getDate: function(date) {
      if (date) {
        let split_date = date.split("-");
        return `${split_date[1]}/${split_date[2]}/${split_date[0]}`;
      }
    },
    getMonth: function(date) {
      if (date) {
        let split_date = date.split("-");
        if (split_date[1] == 1) {
          return "Winter";
        } else if (split_date[1] == 3) {
          return "Spring";
        } else if (split_date[1] == 6) {
          return "Summer";
        } else if (split_date[1] == 9) {
          return "Fall";
        }
      }
    },
    makeMap: function() {
      var thisThis = this;
      Vue.nextTick(function() {
        var map = new ol.Map({
          target: thisThis.$refs.smolMap,
          layers: [
            new ol.layer.Tile({
              source: new ol.source.OSM()
            }),
            new ol.layer.Vector({
              source: new ol.source.Vector({
                features: [
                  new ol.Feature({
                    geometry: new ol.geom.Point(
                      ol.proj.fromLonLat([
                        thisThis.listing.longitude,
                        thisThis.listing.latitude
                      ])
                    ),
                    style: new ol.style.Style({})
                  })
                ]
              })
            })
          ],
          view: new ol.View({
            center: ol.proj.fromLonLat([
              thisThis.listing.longitude,
              thisThis.listing.latitude
            ]),
            zoom: 15
          })
        });
      });
    },
    toggleMap: function() {
      this.showMap = !this.showMap;
      if (!this.mapReady) {
        this.mapReady = true;
        this.makeMap();
      }
    }
  }
};
</script>
