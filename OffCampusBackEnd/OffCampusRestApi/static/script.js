$(document).ready(function(){
    $('select').formSelect();
});

$(document).ready(function(){
    $.ajax({

    })
});

$('#signinButton').click(function() {
    auth2.grantOfflineAccess().then(signInCallback);
});

function signInCallback(authResult) {
  if (authResult['code']) {
    $.ajax({
      type: 'POST',
      url: 'http://example.com/storeauthcode',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      },
      contentType: 'application/octet-stream; charset=utf-8',
      success: function(result) {
          
      },
      processData: false,
      data: authResult['code']
    });
  } else {

  }
}

function goToPage(page)
{
    const urlParams = new URLSearchParams(window.location.search);
    if(urlParams.has('page'))
    {
        urlParams.set('page', page);
    }
    else
    {
        urlParams.append('page', page);
    }
    console.log("/?" + urlParams.toString());
    window.location.href = window.location.origin + "?"  + urlParams.toString();
}

function restoreFilters()
{
    const urlParams = new URLSearchParams(window.location.search);
    $("#bedrooms").val(urlParams.get('beds'));
    if(urlParams.get('beds'))
    {
        $("#bedrooms").siblings().addClass('active');
    }
    $("#bathrooms").val(urlParams.get('baths'));
    if(urlParams.get('baths'))
    {
        $("#bathrooms").siblings().addClass('active');
    }
    $("#min-price").val(urlParams.get('minPrice'));
    if(urlParams.get('minPrice'))
    {
        $("#min-price").siblings().addClass('active');
    }
    $("#max-price").val(urlParams.get('maxPrice'));
    if(urlParams.get('maxPrice'))
    {
        $("#max-price").siblings().addClass('active');
    }
    if(urlParams.get('showNoPrice') === "true") $("#show-no-price").prop('checked', true);
    else if(!urlParams.has('showNoPrice')) $("#show-no-price").prop('checked', true);
    else $("#show-no-price").prop('checked', false);
    $("#min-distance").val(urlParams.get('minDistance'));
    if(urlParams.get('minDistance'))
    {
        $("#min-distance").siblings().addClass('active');
    }
    $("#max-distance").val(urlParams.get('maxDistance'));
    if(urlParams.get('maxDistance'))
    {
        $("#max-distance").siblings().addClass('active');
    }

    $("#sort").val(urlParams.get('order'));
    $('#sort').formSelect();
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
    var sort = $('#sort').val()
    var params = $.param({'beds':beds, 'baths':bath, 'minPrice':minPrice, 'maxPrice':maxPrice, 'showNoPrice':showNoPrice, 'minDistance':minDistance, 'maxDistance':maxDistance, 'order': sort});
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

// this code is jank af
function twoVal(one, two) {
    var oneNum = parseInt(one)
    var twoNum = parseInt(two)
    if ((oneNum.length > 0 && oneNum == NaN) || (twoNum.length > 0 && twoNum == NaN)) {
        // they entered something but it was invalid
        return false
    }
    if(one.length === 0 && two.length === 0)
    {
        return true;
    }
    else if(one.length > 0 && two.length === 0)
    {
        return true;
    }
    else if(one.length === 0 && two.length > 0)
    {
        return true;
    }
    else if(one.length > 0 && two.length > 0 && oneNum >= 0 && twoNum > 0 && oneNum < twoNum)
    {
        return true;
    }
    return false
}

var mapLoaded = false
function makeBigMap(results) {
    mapLoaded = true
    var features = []
    //var instances = M.Tooltip.init(document.getElementById("popup"), {});

    var iconStyle = new ol.style.Style({});

    for (listing of results) {
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

function loadMap() {
    if (!mapLoaded) {
        const urlParams = new URLSearchParams(window.location.search);
        $.get('/query_json'+window.location.search).done(function (data) {
            console.log(data)
            makeBigMap(data);
        })
    }
}
