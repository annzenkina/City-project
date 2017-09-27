function renderStatus(statusText) {
  document.getElementById('status').textContent = statusText;
}

function geoSuccess(position) {
  // console.log(position);
  renderStatus("lat: " + position.coords.latitude + " lng: " + position.coords.longitude);

  var data = new FormData();
  data.append('latitude', position.coords.latitude);
  data.append('longitude', position.coords.longitude);

  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:8000', true);
  xhr.onload = function () {
      // console.log(this.responseText);
      renderStatus(this.responseText);
  };
  xhr.send(data);
};

document.addEventListener('DOMContentLoaded', function() {
  renderStatus("Waiting for coordinates...");
  navigator.geolocation.getCurrentPosition(geoSuccess);
});
