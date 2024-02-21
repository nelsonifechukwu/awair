// Dashboard Map
var long = JSON.parse(document.getElementById("long").textContent);
// console.log(long);
var lat = JSON.parse(document.getElementById("lat").textContent);
var deviceId = JSON.parse(document.getElementById("dev").textContent);
// var place = JSON.parse(document.getElementById("place").textContent);
var id = JSON.parse(document.getElementById("id").textContent);
// console.log(lat);
var lat = parseFloat(lat);
var long = parseFloat(long);

var allVal = {
  temperature: 0,
  pressure: 0,
  humidity: 0,
  windSpeed: 0,
  windDirection: 0,
  pmtwo: 0,
  pmten: 0,
  co: 0,
  place: "None",
};
var map = L.map("map", {
  fullscreenControl: true,
  fullscreenControlOptions: {
    position: "topleft",
  },
}).setView([lat, long], 13);
// DON'T FORGET TO ADD ICONS FOR THE VARIABLES.

var customIcon = L.divIcon({
  className: "custom-icon",
  html: '<div><i class="fas fa-book-open" style="font-size:30px"></i></div>',
  iconSize: [30, 30],
  iconAnchor: [15, 10],
});
// L.marker([lat,long], {icon: customIcon}).bindPopup(L.popup({maxWidth:500}).setContent(popupItem)).addTo(map);

L.tileLayer(
  "http://sgx.geodatenzentrum.de/wmts_topplus_open/tile/1.0.0/web/default/WEBMERCATOR/{z}/{y}/{x}.png",
  {
    maxZoom: 18,
    attribution:
      'Map data: &copy; <a href="http://www.govdata.de/dl-de/by-2-0">dl-de/by-2-0</a>',
  }
).addTo(map);

// for various markers
var markers = {};
function getMarkers(positionData) {
  for (var ids in positionData) {
    var data = positionData[ids];
    var otherLat = parseFloat(data.lat);
    var otherLong = parseFloat(data.long);
    if (!isNaN(otherLat) && !isNaN(otherLong)) {
      if (!markers[ids]) {
        var popupItem = `
      <div>
        <div style="text-align: center">
          <i class="fas fa-location-dot"></i>&nbsp;<span
            style="font-size: 12px; font-weight: 500"
            id="${ids}placeval">
            ${allVal.place}</span>
        </div>
        <hr style="margin: 7px 0px" />

        <div class="pop-container">
          <div>Temperature</div>
          <div><span id="${ids}tempval">${allVal.temperature}</span>&deg;C</div>

          <div>Humidity</div>
          <div><span id="${ids}humval">${allVal.humidity}</span> %</div>

          <div class = "pop-item">Pressure</div>
          <div class = "pop-item"><span id="${ids}presval">${allVal.pressure}</span> Kpa</div>

          <div>PM2.5</div>
          <div><span id="${ids}pmtwoval">${allVal.pmtwo}</span> µg/m<sup>3</sup></div>

          <div>PM10</div>
          <div><span id="${ids}pmtenval">${allVal.pmten}</span> µg/m<sup>3</sup></div>

          <div class = "pop-item">CO</div>
          <div class = "pop-item"><span id="${ids}coval">${allVal.co}</span> ppm</div>

          <div>Wind Direction</div>
          <div><span id="${ids}direction">${allVal.windDirection}</span>&deg;</div>

          <div>Wind speed</div>
          <div><span id="${ids}speed">${allVal.windSpeed}</span> ms<sup>-1</sup></div>

          <div>Cloud</div>
          <div><span id="${ids}cloud_cover">${allVal.cloud_cover}</span> %</div>
        </div>
      </div>
`;
        markers[ids] = L.marker([otherLat, otherLong], { icon: customIcon })
          .addTo(map)
          .bindPopup(L.popup({ maxWidth: 500 }).setContent(popupItem))
          .addTo(map);
      }
    }
  }
}

function getAlldata() {
  $.ajax({
    url: "/dashboard/" + id + "/map/all",
    method: "GET",
    dataType: "json",
    success: function (data) {
      for (let id in data) {
        var values = data[id];
        allVal.temperature = values.temperature;
        allVal.pressure = values.pressure;
        allVal.humidity = values.humidity;
        allVal.pmtwo = values.pmtwo;
        allVal.pmten = values.pmten;
        allVal.co = values.co;
        allVal.windSpeed = values.wind_speed;
        allVal.windDirection = values.wind_direction;
        allVal.place = values.place;
        $("#" + id + "tempval").text(allVal.temperature);
        $("#" + id + "humval").text(allVal.pressure);
        $("#" + id + "presval").text(allVal.humidity);
        $("#" + id + "pmtwoval").text(allVal.pmtwo);
        $("#" + id + "pmtenval").text(allVal.pmten);
        $("#" + id + "coval").text(allVal.co);
        $("#" + id + "speed").text(allVal.windSpeed);
        $("#" + id + "direction").text(allVal.windDirection);
        $("#" + id + "placeval").text(allVal.place);
      }
    },
    error: function (error) {
      console.error("Error getting data: ", error);
    },
  });
}

getAlldata();
setInterval(getAlldata, 3000);
function getLocations() {
  $.ajax({
    url: "/dashboard/" + id + "/locations",
    method: "GET",
    dataType: "json",
    success: function (data) {
      getMarkers(data);
    },
    error: function (error) {
      console.error("Error getting data: ", error);
    },
  });
}
getLocations();
