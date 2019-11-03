$('#bigmap').toggle()
function restoreFilters()
{
    const urlParams = new URLSearchParams(window.location.search);
    $("#bedrooms").val(urlParams.get('beds'));
    $("#bathrooms").val(urlParams.get('baths'));
    $("#min-price").val(urlParams.get('minPrice'));
    $("#max-price").val(urlParams.get('maxPrice'));
    if(urlParams.get('showNoPrice') === "True") $("#show-no-price").prop('checked', true);
    else $("#show-no-price").prop('checked', false);
    $("#min-distance").val(urlParams.get('minDistance'));
    $("#max-distance").val(urlParams.get('maxDistance'));
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

function toggleBigMap() {
    loadMap();
    $('#bigmap').toggle();
}

$('td.map').each(function () {
    var latitude = $(this).attr('latitude');
    var longitude = $(this).attr('longitude');

    if (latitude && longitude) {
        renderMap(this, latitude, longitude)
    }
})

function reloadWithParams(e)
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
    e.preventDefault()
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

var mapLoaded = false
function makeBigMap(results) {
    mapLoaded = true
    var features = []
    var instances = M.Tooltip.init(document.getElementById("popup"), {});

    var iconStyle = new ol.style.Style({});

    for (listing of results) {
        var l = listing.fields
        var latitude = l["latitude"]
        var longitude = l["longitude"]
        var address = l["address"]
        if (latitude && longitude) {
            var iconFeature = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([longitude, latitude])),
                name: address,
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

    

    var bigMap = new ol.Map({
        target: document.getElementById("bigmap"),
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            }),
            vectorLayer
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([-83.0, 40.0]),
            zoom: 14
        })
    });

    var popup = new ol.Overlay({
        element: document.getElementById("popup"),
        positioning: 'bottom-center',
        stopEvent: false,
        offset: [0, -50]
      });
      bigMap.addOverlay(popup);

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
            $(pu).tooltip({html: feature.get('name')});
            $(pu).tooltip("open")
        } else {
            $(pu).tooltip("close")
        }
    });
    
    // change mouse cursor when over marker
    bigMap.on('pointermove', function(e) {
        if (e.dragging) {
        $(element).popover('destroy');
        return;
        }
        var pixel = bigMap.getEventPixel(e.originalEvent);
        var hit = bigMap.hasFeatureAtPixel(pixel);
        bigMap.getTarget().style.cursor = hit ? 'pointer' : '';
    });
}

function loadMap() {
    if (!mapLoaded) {
        const urlParams = new URLSearchParams(window.location.search);
        $.get('/query_json'+window.location.search).done(function (data) {
            console.log(data)
            makeBigMap(data);
        })
    }
}
