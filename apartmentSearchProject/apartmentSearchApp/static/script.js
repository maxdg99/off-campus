function reloadWithParams()
{
    var beds = $("#bedrooms").val();
    var bath = $("#bathrooms").val();
    var minPrice = $("#min-price").val();
    var maxPrice = $("#max-price").val();
    var showNoPrice = $("#show-no-price").val();
    var minDistance = $("#min-distance").val();
    var maxDistance = $("#min-distance").val();
    var params = $.param({'beds':beds, 'bath':bath, 'minPrice':minPrice, 'maxPrice':maxPrice, 'showNoPrice':showNoPrice, 'minDistance':minDistance, 'maxDistance':maxDistance});
    console.log(params);
    if(!isNaN(beds) && !isNaN(bath) && !isNaN(minPrice) && !isNaN(maxPrice) && !isNaN(minDistance) && !isNaN(maxDistance) &&
        beds > 0 && bath > 0 && minPrice > 0 && minPrice < maxPrice && minDistance > 0 && minDistance < maxDistance){
            window.location.href = window.location.pathname+"?"+$.param({'foo':'bar','base':'ball'})
    }
    else{
        alert("Hmm, your filters don't seem right.  Can you double check?")
    }
}

function renderMap(mapElement, latitude, longitude) {
    var map = new ol.Map({
        target: mapElement,
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            }),
            new ol.layer.Vector({
                source: new ol.source.Vector({
                    features: [new ol.Feature({
                        geometry: new ol.geom.Point(ol.proj.fromLonLat([longitude, latitude]))
                    })]
                })
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([longitude, latitude]),
            zoom: 15
        })
    });
}

$('td.map').each(function () {
    var latitude = $(this).attr('latitude');
    var longitude = $(this).attr('longitude');

    if (latitude && longitude) {
        renderMap(this, latitude, longitude)
    }
})