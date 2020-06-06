<template>
  <div class="uk-card uk-card-small uk-card-default uk-card-hover">
    <div class="uk-card-media-top">
      <img v-bind:src="listing.image" v-show="!showMap" uk-img />
      <div v-show="showMap" ref="smolMap" />
    </div>
    <div class="uk-card-body">
      <div class="listing-info-container">
        <div v-if="listing.price">${{ listing.price }}</div>
        <div v-else>N/A</div>
        <div>
          <div>{{ listing.miles_from_campus }} mi</div>
          <div>&nbsp;|&nbsp;</div>
          <div>{{ `${listing.beds} ${listing.beds==1 ? "bed" : "beds"}` }}</div>
          <div>&nbsp;|&nbsp;</div>
          <div>{{ `${listing.baths} ${listing.baths==1 ? "bath" : "baths"}` }}</div>
        </div>
      </div>
      <div>
        <a v-bind:href="listing.url" target="_blank">{{ listing.pretty_address }}</a>
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
      <a uk-icon="location" v-on:click="toggleMap" v-show="canFlip"></a>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/scss/_variables.scss";

/* Image and map */
.uk-card-media-top {
  & > * {
    height: 200px;
  }

  & > img {
    width: 100%;
    object-fit: cover;
  }
}

.uk-card-body {
  padding: 5px 10px 10px 10px;
  font-weight: 600;
  color: black;
}

.listing-info-container {
  display: flex;
  justify-content: space-between;
  align-items: center;

  /* Price */
  & > *:first-child {
    font-size: 1.75em;
  }

  /* Distance, beds, baths */
  & > *:last-child {
    display: flex;
    flex-wrap: wrap;
    white-space: pre;
    margin-left: 10px;
  }
}

/* Address */
a,
a:hover {
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
    listing: Object,
    canFlip: {
      type: Boolean,
      default: true
    }
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
