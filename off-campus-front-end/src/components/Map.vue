<template>
<div id="bigmap" v-show="displayed">
    <div id="popup">
        <div class="card" id="popup-content" style="display: none;">
            <!-- Card Content -->
        </div>
    </div>
</div>
</template>

<style scoped>
/* #bigmap {
    height: 50%;
} */
#bigmap {
    height: 200px;
    width: 100%;
}
</style>

<script>
import axios from "axios";

export default {
    data: function () {
        return {
            filters: null,
            displayed: false
        }
    },
    methods: {
        toggleMap: function() {
            this.loadMap();
            this.displayed = true
        },
        loadMap: function() {
            if (!this.mapLoaded) {
                this.mapLoaded = true;
                axios({
                    method: "GET",
                    url: "http://localhost:8000/allListings",
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
                        this.makeBigMap(result.data)
                    },
                    error => {
                        console.error(error);
                        this.searching = false;
                    }
                );
            }
        },
        makeBigMap: function (results) {
            this.mapLoaded = true
            var features = []
            //var instances = M.Tooltip.init(document.getElementById("popup"), {});

            var iconStyle = new ol.style.Style({});

            for (let listing of results) {
                var l = listing.fields
                var latitude = l["latitude"]
                var longitude = l["longitude"]
                var address = l["address"]
                var overlayHTML = ""
                overlayHTML += "<a href=\""+l["url"]+"\" target=\"_blank\"><strong>" + address + "</strong></a><div class=\"row\">";
                overlayHTML += "<div class=\"col s6\"><p style=\"text-align: left;\">"+l["num_bedrooms"]+" bed, " + l["num_bathrooms"] + " bath</p></div>";
                if (l["image_url"]) {
                    overlayHTML += "<div class=\"col s6\"><img style=\"text-align: right;\" src=\""+l["image_url"]+"\" width=80px></img></div></div>"
                }
                //overlayHTML += "<div class=\"btn\" href=\""+l["url"]+"\">b</div>";


                if (latitude && longitude) {
                    var iconFeature = new ol.Feature({
                        geometry: new ol.geom.Point(ol.proj.fromLonLat([longitude, latitude])),
                        name: overlayHTML,
                        population: 4000,
                        rainfall: 500,
                        style: iconStyle
                    });
                
                    //iconFeature.setStyle(iconStyle);
                    features.push(iconFeature)
                }
            }

            var vectorSource = new ol.source.Vector({
            features: features
            });

            var vectorLayer = new ol.layer.Vector({
            source: vectorSource
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
                // display popup on click
            bigMap.on('click', function(evt) {
                var feature = bigMap.forEachFeatureAtPixel(evt.pixel,
                    function(feature) {
                        return feature;
                    });
                var pu = document.getElementById("popup")
                if (feature) {
                    var coordinates = feature.getGeometry().getCoordinates();
                    popup.setPosition(coordinates);
                    $('#popup-content').html(feature.get('name'))
                    $('#popup-content').show()
                } else {
                    $('#popup-content').hide()
                }
            });
            
            // change mouse cursor when over marker
            bigMap.on('pointermove', function(e) {
                if (e.dragging) {
                    $('#popup-content').hide()
                return;
                }
                var pixel = bigMap.getEventPixel(e.originalEvent);
                var hit = bigMap.hasFeatureAtPixel(pixel);
                bigMap.getTarget().style.cursor = hit ? 'pointer' : '';
            });
        }
    },
    shouldComponentUpdate: function() {
        return true
    }
}
</script>