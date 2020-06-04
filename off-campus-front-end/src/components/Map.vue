<template>
<div id="bigmap">
    <div id="popup">
        <Listing :id="selectedListing.pk" :listing="selectedListing.fields" v-if="selectedListing !== null" :canFlip=false />
    </div>
</div>
</template>

<style scoped>
#popup {
    max-width: 200px;
}
</style>

<script>
import axios from "axios";
import Vue from "vue";
import Listing from "@/components/Listing.vue";

// Style for the little circles on the map
const iconStyle = new ol.style.Style({
    image: new ol.style.Circle({
        radius: 5,
        fill: new ol.style.Fill({color: 'rgba(0, 0, 0, 0.05)'}),
        stroke: new ol.style.Stroke({color: '#607580', width: 1})
    })
});

const selectedStyle = new ol.style.Style({
    image: new ol.style.Circle({
        radius: 7,
        fill: new ol.style.Fill({color: '#0081C2'}),
    })
});

export default {
  components: {
    Listing,
  },
    data: function () {
        return {
            filters: null,
            map: null,
            vectorSource: null,
            mapLoaded: false,
            features: [],
            selectedListing: null,
            featureForListingID: {},
            highlightedFeature: null
        }
    },
    mounted: function () {
        if (!this.mapLoaded) {
            this.makeBigMap();
        }
    },
    methods: {
        loadMap: function() {
            axios({
                method: "GET",
                url: process.env.VUE_APP_API_URL + "/allListings",
                params: {
                beds: this.filters.bedrooms,
                baths: this.filters.bathrooms,
                minPrice: this.filters.minPrice,
                maxPrice: this.filters.maxPrice,
                minDistance: this.filters.minDistance,
                maxDistance: this.filters.maxDistance,
                showNoPrice: this.filters.showWithoutPrice,
                order: this.filters.sortBy
                }
            }).then(
                result => {
                    this.updateMapResults(result.data)
                },
                error => {
                    console.error(error);
                    this.searching = false;
                }
            );
        },
        updateMapResults: function (results) {
            if (!this.mapLoaded) {
                return
            }

            this.features = []
            this.featureForListingID = {}
            for (let listing of results) {
                var latitude = listing.fields.latitude
                var longitude = listing.fields.longitude
                if (latitude && longitude) {
                    var iconFeature = new ol.Feature({
                        geometry: new ol.geom.Point(ol.proj.fromLonLat([longitude, latitude])),
                        name: listing,
                        style: iconStyle
                    });
                    iconFeature.setStyle(iconStyle)
                
                    //iconFeature.setStyle(iconStyle);
                    this.features.push(iconFeature)
                    this.featureForListingID[listing.pk] = iconFeature
                }
                this.vectorSource.refresh()
            }
        },
        makeBigMap: function () {
            //var instances = M.Tooltip.init(document.getElementById("popup"), {});
            
            var thisThis = this;
            this.vectorSource = new ol.source.Vector({loader: function (extent, resolution, projection) {
                thisThis.vectorSource.clear()
                thisThis.vectorSource.addFeatures(thisThis.features)
            }});


            var vectorLayer = new ol.layer.Vector({
                source: this.vectorSource
            });

            var popup = new ol.Overlay({
                element: document.getElementById("popup"),
                positioning: 'bottom-center',
                stopEvent: true,
                offset: [0, 0]
            });

            var bigMap = new ol.Map({
                target: document.getElementById("bigmap"),
                layers: [
                    new ol.layer.Tile({
                        source: new ol.source.OSM()
                    }),
                    vectorLayer
                ],
                overlays: [popup],
                view: new ol.View({
                    center: ol.proj.fromLonLat([-83.0, 40.0]),
                    zoom: 14
                }),
                insertFirst: true
            });

            var vueMap = this;
            // display popup on click
            bigMap.on('click', function(evt) {
                var feature = bigMap.forEachFeatureAtPixel(evt.pixel,
                    function(feature) {
                        return feature;
                    });
                var pu = document.getElementById("popup")
                if (feature) {
                    // Time to show the popup... first figure out where it goes
                    var coordinates = feature.getGeometry().getCoordinates();

                    // Now for some magic: we want the overlay to be fully visible...
                    var extent = bigMap.getView().calculateExtent(bigMap.getSize())
                    var xSize = extent[2] - extent[0]
                    var ySize = extent[3] - extent[1]

                    // This should be built into the fucking library but it's NOT
                    // so I'm doing it myself
                    //
                    // This positions the popup so that it's as visible as possible
                    // without being obtrusive.
                    if ((coordinates[0] - extent[0]) > 2*xSize/3.0) {
                        // Right half of screen
                        if ((coordinates[1] - extent[1]) > 2*ySize/3) {
                            // Top half of screen
                            popup.setPositioning('top-right')
                        } else if ((coordinates[1] - extent[1]) < ySize/3) {
                            // Bottom Half of screen
                            popup.setPositioning('bottom-right')
                        } else {
                            // Centered vertically
                            popup.setPositioning('center-right')
                        }
                    } else if ((coordinates[0] - extent[0]) < xSize/3.0) {
                        // Left half of screen
                        if ((coordinates[1] - extent[1]) > 2*ySize/3) {
                            // Top half of screen
                            popup.setPositioning('top-left')
                        } else if ((coordinates[1] - extent[1]) < ySize/3) {
                            // Bottom Half of screen
                            popup.setPositioning('bottom-left')
                            console.log("BL")
                        } else {
                            // Centered vertically
                            popup.setPositioning('center-left')
                            console.log("CL")
                        }
                    } else {
                        // Centered horizontally
                        if ((coordinates[1] - extent[1]) > 2*ySize/3) {
                            // Top half of screen
                            popup.setPositioning('top-center')
                        } else if ((coordinates[1] - extent[1]) < ySize/3) {
                            // Bottom Half of screen
                            popup.setPositioning('bottom-center')
                        } else {
                            // Centered vertically
                            popup.setPositioning('center-center')
                        }

                    }
                    
                    vueMap.selectedListing = feature.get('name')
                    Vue.nextTick(function () {
                        popup.setPosition(coordinates);
                    })
                } else {
                    vueMap.selectedListing = null
                }
            });
            
            // change mouse cursor when over marker
            bigMap.on('pointermove', function(e) {
                if (e.dragging) {
                    // This makes the overlay disappear
                    vueMap.selectedListing = null
                    return;
                }
                var pixel = bigMap.getEventPixel(e.originalEvent);
                var hit = bigMap.hasFeatureAtPixel(pixel);
                bigMap.getTarget().style.cursor = hit ? 'pointer' : '';
            });

            this.map = bigMap
            this.mapLoaded = true
        },
        highlightListing: function (listingID) {
            // Restore old style
            if (this.highlightedFeature) {
                this.highlightedFeature.setStyle(iconStyle)
                this.highlightedFeature = null
            }
            // First we have to find the OpenLayers 'feature' corresponding to this listing
            // ID... because I took CSE 2331 I know I want a map!
            let feature = this.featureForListingID[listingID]
            if (feature) {
                feature.setStyle(selectedStyle)
            }
            this.highlightedFeature = feature


        }
    },
    shouldComponentUpdate: function() {
        return true
    }
}
</script>