<template>
  <div class="uk-card uk-card-small uk-card-default uk-card-hover">
    <ul class="uk-subnav uk-subnav-pill switcher" uk-switcher>
          <li><a href="#">Image</a></li>
          <li><a href="#">Map</a></li>
    </ul>
      <ul class="uk-switcher switcher-container uk-margin">
        <li>
            <div class="uk-card-media-top">
              <img v-bind:src="listing.image_url" class="listing-image" />
            </div>
        </li>
        <li>
          <div id="map">
           
          </div>
        </li>
      </ul>
    <div class="uk-card-body listing-body">
      <div class="price-info-container">
        <div v-if="listing.price" class="listing-price">${{ listing.price }}</div>
        <div v-else>N/A</div>
        <span class="listing-info-container">
            <div class="listing-info">{{ listing.miles_from_campus }} mi</div> |
            <div class="listing-info">{{ `${listing.num_bedrooms} ${listing.num_bedrooms==1 ? "bed" : "beds"}` }}</div> |
            <div class="listing-info">{{ `${listing.num_bathrooms} ${listing.num_bathrooms==1 ? "bath" : "baths"}` }}</div>
        </span>
      </div>
      <div class="listing-address-parent">
        <a v-bind:href="listing.url" target="_blank" class="listing-address">{{ listing.address }}</a>
      </div>
      <div class="listing-availability-parent">
        <div class="listing-availability" v-if="listing.availability_mode=='S'">Available this {{getMonth(listing.availability_date.month)}}</div>
        <div class="listing-availability" v-else-if="listing.availability_mode=='M'">Available in {{this.months[listing.availability_date.month - 1]}}</div>
        <div class="listing-availability" v-else-if="listing.availability_mode=='N'">Available Now</div>
        <div class="listing-availability" v-else-if="listing.availability_mode=='D'">Available on {{getDate(listing.availability_date)}}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
:root {
  --card-section-margin: 10px;
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
import Vue from 'vue'
import VueLayers from 'vuelayers'
import 'vuelayers/lib/style.css' // needs css-loader

Vue.use(VueLayers)

export default {
  name: "Listing",
  data: function () {
    return {
      months: ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    }
  },
  props: {
    id: Number,
    listing: Object
  },
  created: function () {
    var map = new OpenLayers.Map("map");
    map.addLayer(new OpenLayers.Layer.OSM());
    map.zoomToMaxExtent();
  },
  methods: {
    getDate(date) {
      var split_date = date.split("-")
      return `${split_date[1]}\\${split_date[2]}\\${split_date[0]}`
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
