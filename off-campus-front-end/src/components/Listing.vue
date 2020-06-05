<template>
  <div class="uk-card uk-card-small uk-card-default uk-card-hover uk-card-body">
    <div class="listing-address-parent">
      <a v-bind:href="listing.url" target="_blank" class="listing-address">{{ listing.address }}</a>
    </div>
    <img v-bind:src="listing.image" class="listing-image" v-show="!showMap" />
    <div class="listing-map" v-show="showMap" ref="smolMap" />
    <div class="listing-info-container">
      <div class="listing-info-row">
        <div v-if="listing.price" class="listing-info listing-price">${{ listing.price }}</div>
        <div v-else class="listing-info">N/A</div>
        <div class="listing-info">{{ listing.miles_from_campus }} mi</div>
      </div>
      <div class="listing-info-row">
        <div class="listing-info">{{ listing.beds }} beds</div>
        <div class="listing-info">{{ listing.baths }} baths</div>
      </div>
    </div>
    <div class="map-icon">
      <a uk-icon="location" v-on:click="toggleMap" v-show="canFlip"></a>
    </div>
  </div>
</template>

<style scoped>
:root {
  --card-section-margin: 10px;
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

.map-icon {
  position: absolute;
  right: 20px;
  bottom: 20px;

}
.listing-map {
  height: 200px;
}

/* Special Style for use in Big Map */
#popup .listing-image {
  height: 100px;
}

#popup .listing-info-container {
  margin-left: 0;
  margin-right: 0;
  font-size: 0.8em;
}

#popup .listing-address,
#popup .listing-address:hover {
  font-size: 0.8em;
}


</style>

<script>
import Vue from "vue";

export default {
  name: "Listing",
  props: {
    id: Number,
    listing: Object,
    canFlip: {
      type: Boolean,
      default: true
    }
  },
  data: function () {
    return {showMap: false, mapReady: false}
  },
  mounted: function() {
    
  },
  methods: {
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
  }
};
</script>
