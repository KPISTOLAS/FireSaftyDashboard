// Initialize map with Kavala coordinates
const map = L.map('map').setView([40.95, 24.5], 10);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18,
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Nodes injected by template
const nodes = window.NODES || [];

const createNodeIcon = (isParent) => {
  return L.divIcon({
    className: isParent ? 'home-icon' : 'marker-icon',
    html: `<i class="fas ${isParent ? 'fa-home' : 'fa-circle'}"></i>`,
    iconSize: isParent ? [30, 30] : [20, 20],
    iconAnchor: isParent ? [15, 15] : [10, 10]
  });
};

const getNodeUrl = (nodeId, isParent) => {
  const formattedId = nodeId.slice(1).replaceAll('_', '.');
  return isParent ? `/parent/${formattedId}` : `/node/${formattedId}`;
};

const parentCoords = {};

nodes.forEach(node => {
  if (!node.lat || !node.lng) return;
  const isParent = node.is_parent === true || node.is_parent === 'true';
  if (isParent) {
    parentCoords[node.node_id] = {
      lat: parseFloat(node.lat),
      lng: parseFloat(node.lng)
    };
  }
});

nodes.forEach(node => {
  if (!node.lat || !node.lng) return;
  const lat = parseFloat(node.lat);
  const lng = parseFloat(node.lng);
  const isParent = node.is_parent === true || node.is_parent === 'true';
  const label = node.title || node.node_id;
  const url = getNodeUrl(node.node_id, isParent);

  L.marker([lat, lng], { icon: createNodeIcon(isParent) })
    .addTo(map)
    .bindTooltip(label, { direction: 'top', offset: [0, -10], opacity: 0.9 })
    .on('click', () => { window.location.href = url; });

  if (!isParent && node.node_id.includes('_')) {
    const parentId = 'N' + node.node_id.split('_')[0].slice(1);
    if (parentCoords[parentId]) {
      L.polyline([[lat, lng], [parentCoords[parentId].lat, parentCoords[parentId].lng]], {
        color: 'red',
        weight: 2,
        dashArray: '5,5'
      }).addTo(map);
    }
  }
});

function updateTime() {
  const now = new Date();
  const timeString = now.toLocaleTimeString('el-GR');
  const dateString = now.toLocaleDateString('el-GR');

  const timeElement = document.getElementById('db-update-time');
  const currentTimeElement = document.getElementById('current-time');
  const currentDateElement = document.getElementById('current-date');

  if (timeElement) timeElement.textContent = timeString;
  if (currentTimeElement) currentTimeElement.textContent = timeString;
  if (currentDateElement) currentDateElement.textContent = dateString;
}

setInterval(updateTime, 1000);
updateTime();

