// Wind  (Might use line graphs with arrows as intersections specifying direction)
function graphWind(windData, time) {
  var customImage = new Image(10, 12);
  customImage.src = '/static/assets/arrow_up_thick.png';
  const wind_data = {
    labels: windData.map(entry => entry.date),
    datasets: [{
      label: 'Wind Speed (m/s) & Direction (°)',
      data: windData.map(entry => entry.speed),
      borderColor: 'grey',
      borderWidth: 1,

      fill: true,
      pointStyle: customImage,
      rotation: windData.map(entry => entry.direction),
      pointRadius: 18,
      cubicInterpolationMode: 'monotone',
      tension: 0.4
    }]

  };
  if (time == '1') {
    wind.options.scales.x.time.unit = 'hour';
  }
  else if (time == '7') {
    wind.options.scales.x.time.unit = 'day';
  }
  else if (time == '4') {
    wind.options.scales.x.time.unit = 'month';
  }
  else if (time == '52') {
    wind.options.scales.x.time.unit = 'year';
  }
  wind.data = wind_data;
  wind.update();
}

const options = {
  responsive: true,
  maintainAspectRatio: false,

  scales: {
    x: {
      type: 'time',
      time: {
        unit: 'hour',
        displayFormats: {
          day: 'YYYY-MM-DD'
        }
      },
      title: {
        display: false,
        text: 'Date'
      },
      grid: {
        drawOnChartArea: false,
      }
    },
    y: {
      title: {
        display: false,
        text: 'Wind Speed (m/s)'
      }
    }
  },
  plugins: {
    legend: {
      display: true,
    },
    title: {
      display: true,
      text: 'Wind 💨'
    },
    tooltip: {
      callbacks: {
        label: function (context) {
          const label = context.dataset.label || '';
          if (label) {
            return `${label}: ${context.formattedValue} \n Wind Direction:${context.dataset.rotation[context.dataIndex]}`;
          }
          return context.formattedValue;
        }
      }

    }

  }
};
const wind_data = {
  labels: [],
  datasets: []
}

const ctx2 = document.getElementById('wind');
const wind = new Chart(ctx2, {
  type: 'line',
  data: wind_data,
  options: options
});

// Date Difference
const dateHolderWind = {
  'old': 0,
};

function dateDiff(oldDate, newDate) {
  const labelDate = Math.floor(new Date(oldDate).getTime());
  const dateDate = Math.floor(new Date(newDate).getTime());
  if (dateDate > labelDate) {
    return true;
  }
  else {
    return false;
  }
}

function updateWind(wind_data) {
  wind.data.labels.push(wind_data.date);
  wind.data.datasets[0].data.push(wind_data.speed)
  wind.data.datasets[0].rotation.push(wind_data.direction)
  wind.update();
}

// Ajax
function fetchWind() {
  $.ajax({
    url: '/dashboard/' + id + '/' + deviceId + '/charts/1/wind',
    method: 'GET',
    dataType: 'json',
    success: function (data) {
      graphWind(data);
      var windDate = data.map(d => d.date);
      var labelIndex = windDate.length - 1;
      dateHolderWind.old = windDate[labelIndex];
    },
    error: function (error) {
      console.error('Error fetching data: ', error);
    }
  });
}
fetchWind();

function updateWindByTimeRange(time) {
  $.ajax({
    url: '/dashboard/' + id + '/' + deviceId + '/charts/' + time + '/wind',
    method: 'GET',
    dataType: 'json',
    success: function (data) {
      graphWind(data, time);
      var windDate = data.map(d => d.date);
      var labelIndex = windDate.length - 1;
      dateHolderWind.old = windDate[labelIndex];
    },
    error: function (error) {
      console.error('Error fetching data: ', error);
    }
  });
}

function getLatestWind() {
  $.ajax({
    url: '/dashboard/' + id + '/' + deviceId + '/charts/wind/latest',
    method: 'GET',
    dataType: 'json',
    success: function (data) {
      if (dateDiff(dateHolderWind.old, data.date)) {
        updateWind(data);
        dateHolderWind.old = data.date;
      }
    },
    error: function (error) {
      console.error('Error getting data: ', error);
    }
  });
}
getLatestWind();

setInterval(getLatestWind, 3000);