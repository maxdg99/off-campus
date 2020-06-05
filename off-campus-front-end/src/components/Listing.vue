<template>
  <div class="uk-card uk-card-small uk-card-default uk-card-hover">
    <div class="uk-card-media-top">
      <img v-bind:src="listing.image" class="listing-image" v-show="!showMap" uk-img />
      <div class="listing-map" v-show="showMap" ref="smolMap" />
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
    </div>
    <div class="map-icon">
      <a uk-icon="location" v-on:click="toggleMap"></a>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/scss/_variables.scss";

$card-section-margin: 0;
$listing-image-map-height: 200px;

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
  font-size: 1.75rem;
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

  @media screen and (min-width: $min-desktop-screen-width) {
    display: none;
  }
}
</style>

<script>
import Vue from "vue";

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
    listing: Object
  },
  methods: {
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
