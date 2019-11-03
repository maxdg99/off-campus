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

function reloadWithParams()
{
    var beds = $("#bedrooms").val();
    var bath = $("#bathrooms").val();
    var minPrice = $("#min-price").val();
    var maxPrice = $("#max-price").val();
    var showNoPrice = $("#show-no-price").is(':checked');
    var minDistance = $("#min-distance").val();
    var maxDistance = $("#min-distance").val();
    var params = $.param({'beds':beds, 'baths':bath, 'minPrice':minPrice, 'maxPrice':maxPrice, 'showNoPrice':showNoPrice, 'minDistance':minDistance, 'maxDistance':maxDistance});
    if(oneVal(beds) && oneVal(bath) && twoVal(minPrice, maxPrice) && twoVal(minDistance, maxDistance)) {
        window.location.href = window.location.pathname+"?"+params
        $("#submit").css('background', '#666666');
    }
    else {
        $("#submit").css('background', '#bb0000');
    } 
}

function oneVal(num) {
    return num >= 0 || num.length === 0;
}

function twoVal(one, two) {
    if(one.length === 0 && two.length === 0)
    {
        return true;
    }
    else if(one >= 0 && two.length === 0)
    {
        return true;
    }
    else if(one.length === 0 && two.length > 0)
    {
        return true;
    }
    else if(one.length > 0 && two.length > 0 && one >= 0 && two > 0 && one < two)
    {
        return true;
    }
    return false
}