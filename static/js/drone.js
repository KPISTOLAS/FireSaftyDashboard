// Initialize map and drone marker
const map = L.map('map').setView([40.8, 23.5], 7);
L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
  maxZoom: 17,
  attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, SRTM | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a>'
}).addTo(map);

// Image URL injected by template in window.DRONE_IMAGE_URL
const droneIcon = L.icon({
  iconUrl: window.DRONE_IMAGE_URL,
  iconSize: [60, 60],
  iconAnchor: [30, 30],
  className: 'drone-icon'
});

const marker = L.marker([40.8, 23.5], { icon: droneIcon, zIndexOffset: 1000 }).addTo(map);

async function fetchDroneData() {
  try {
    const response = await fetch('/api/drone_telemetry');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching drone data:', error);
    return null;
  }
}

async function updateTelemetry() {
  const data = await fetchDroneData();
  if (!data) return;

  document.getElementById('location').textContent =
    `${data.location.lat.toFixed(4)}° N, ${data.location.lon.toFixed(4)}° E`;
  document.getElementById('altitude').textContent = `${data.location.altitude.toFixed(1)} m`;
  document.getElementById('speed').textContent = `${data.movement.speed.toFixed(1)} m/s`;
  document.getElementById('battery').textContent =
    `${data.battery.percentage.toFixed(0)}% (${data.battery.voltage.toFixed(1)}V)`;

  const fireStatus = document.getElementById('fire-status');
  if (data.fire_detection.detected) {
    fireStatus.textContent = `Ανίχνευση Πυρκαγιάς! (Εμπιστοσύνη: ${(data.fire_detection.confidence * 100).toFixed(0)}%)`;
    fireStatus.className = 'fire-alert';
  } else {
    fireStatus.textContent = 'Κανονική κατάσταση';
    fireStatus.className = '';
  }

  marker.setLatLng([data.location.lat, data.location.lon]);
  map.panTo([data.location.lat, data.location.lon]);

  const now = new Date();
  document.getElementById('last-update').textContent = now.toLocaleTimeString('el-GR');
}

function updateTime() {
  const now = new Date();
  const timeString = now.toLocaleTimeString('el-GR');
  const dateString = now.toLocaleDateString('el-GR');

  const currentTimeElement = document.getElementById('current-time');
  const currentDateElement = document.getElementById('current-date');

  if (currentTimeElement) currentTimeElement.textContent = timeString;
  if (currentDateElement) currentDateElement.textContent = dateString;
}

setInterval(updateTelemetry, 2000);
setInterval(updateTime, 1000);

updateTelemetry();
updateTime();

