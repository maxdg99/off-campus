<template>
  <div class="uk-card uk-card-small uk-card-default uk-card-hover">
    <div class="uk-card-media-top">
      <img v-bind:src="listing.image" class="listing-image" uk-img/>
      <div class="listing-map" v-show="showMap" ref="smolMap" />
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
        <a v-bind:href="listing.url" target="_blank" class="listing-address">{{ listing.address }}</a>
      </div>
      <div class="listing-availability-parent">
        <div class="listing-availability" v-if="listing.availability_mode=='Season'">Available this {{getMonth(listing.availability_date.month)}}</div>
        <div class="listing-availability" v-else-if="listing.availability_mode=='Month'">Available in {{this.months[listing.availability_date.month - 1]}}</div>
        <div class="listing-availability" v-else-if="listing.availability_mode=='Now'">Available Now</div>
        <div class="listing-availability" v-else-if="listing.availability_mode=='Date'">Available on {{getDate(listing.availability_date)}}</div>
      </div>
    </div>
    <div class="map-icon">
      <a uk-icon="location" v-on:click="toggleMap"></a>
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

.map-icon {
  position: absolute;
  right: 20px;
  bottom: 20px;

}
.listing-map {
  height: 200px;
}
</style>

<script>
import Vue from "vue";

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
  methods: {
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
    },
     makeMap: function () {
      var thisThis = this;
      Vue.nextTick(function () {
        var map = new ol.Map({
          target: thisThis.$refs.smolMap,
          layers: [
              new ol.layer.Tile({
                  source: new ol.source.OSM()
              }),
              new ol.layer.Vector({
                  source: new ol.source.Vector({
                      features: [new ol.Feature({
                          geometry: new ol.geom.Point(ol.proj.fromLonLat([thisThis.listing.longitude, thisThis.listing.latitude])),
                          style: new ol.style.Style({})
                      })]
                  })
              })
          ],
          view: new ol.View({
              center: ol.proj.fromLonLat([thisThis.listing.longitude, thisThis.listing.latitude]),
              zoom: 15
          })
        });
      })
    },
    toggleMap: function () {
      this.showMap = !this.showMap
      if (!this.mapReady) {
        this.mapReady = true
        this.makeMap()
      }
    }
  },
  data: function () {
    return {showMap: false, mapReady: false}
  },
  mounted: function() {
    
  }
};
</script>
