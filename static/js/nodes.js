function updateTime() {
  const now = new Date();
  const timeString = now.toLocaleTimeString('el-GR');
  const dateString = now.toLocaleDateString('el-GR');
  const currentTimeElement = document.getElementById('current-time');
  const currentDateElement = document.getElementById('current-date');
  if (currentTimeElement) currentTimeElement.textContent = timeString;
  if (currentDateElement) currentDateElement.textContent = dateString;
}

setInterval(updateTime, 1000);
updateTime();

