// TPH graph
const ctx = document.getElementById('tph');
// const datelabels = labels.map(label => Math.floor(new Date(label).getTime()));
// console.log(datelabels);

function graphTPH(temperature_data, humidity_data, pressure_data, labels, time='1'){
  const temperatureData = {
    label: "Temperature (°C)",
    data: temperature_data,
    borderColor: "blue",
    borderWidth: 0.85,
    pointRadius: 0,
    fill: false,
    // I am using stepped before(Might change this later) and fill false: Might change for other kinds of data
    stepped: true,
    // for curvature of line
    // cubicInterpolationMode: 'monotone',
    // tension:0.4,
  };
  const humidityData = {
    label: 'Humidity (%)',
    data: humidity_data,
    borderColor: 'red',
    borderWidth: 0.85,
    pointRadius: 0,
    fill: false,
    stepped: true,
    // cubicInterpolationMode: 'monotone',
    // tension: 0.4,
  };
  const pressureData = {
    label: 'Pressure (Kpa)',
    data: pressure_data,
    borderColor: 'green',
    borderWidth: 0.85,
    pointRadius: 0,
    fill: false,
    stepped: true,
    // cubicInterpolationMode: 'monotone',
    // tension: 0.4,
  };
  if(time=='1'){
    tph.options.scales.x.time.unit = 'hour';
  }
  else if(time == '7'){
    tph.options.scales.x.time.unit = 'day';
  }
  else if(time == '4'){
    tph.options.scales.x.time.unit = 'month';
  }
  else if(time == '52'){
    tph.options.scales.x.time.unit = 'year';
  }
  tph.data.labels = labels;
  tph.data.datasets[0] = temperatureData;
  tph.data.datasets[1] = humidityData;
  tph.data.datasets[2] = pressureData;
  tph.update();
};


const data = {
  labels: [],
  datasets: []
};

const option = {
  responsive: true,
  maintainAspectRatio: false,
  title: {
display: true,
text: "TP&H data"
  },
  hover: {
    mode: 'nearest'
  },
  tooltips: {
    mode: 'nearest',
    intersect: true
  },
  interaction: {
    intersect: false
  },
  scales: {
    x: {
      type: 'time',
      time: {
        unit: 'hour',
        displayFormats: {
          day: 'YYYY-MM-DD'
        },
      },
      title: {
        display: false,
        text: 'Date'
      },
      grid:{
        drawOnChartArea:false,
      }
    },
    y: {
      title: {
        display: false,
        text: '(0c, Kpa, %)'
      }
    }
  },
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'TP&H'
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const label = context.dataset.label || '';
          if (label) {
            return `${label}: ${context.formattedValue}`;
          }
          return context.formattedValue;
        }
      }
    }
  }
};



const tph = new Chart(ctx, {
  type: 'line',
  
  data:data,
  options:option
  
});
// Date Difference
const dateHolderTPH = {
  'old': 0,
};
function dateDiff(oldDate, newDate){
const labelDate = Math.floor(new Date(oldDate).getTime());
const dateDate = Math.floor(new Date(newDate).getTime());
if(dateDate > labelDate){
  return true;
}
else{
  return false
}
}
// Update Chart
function updateChart(temperature_data, humidity_data, pressure_data, labels){
  tph.data.labels.push(labels);
  
  tph.data.datasets[0].data.push(temperature_data);
  tph.data.datasets[1].data.push(humidity_data);
  tph.data.datasets[2].data.push(pressure_data);
  tph.update();
  

}

// Ajax
var id = JSON.parse(document.getElementById("id").textContent);
var deviceId = JSON.parse(document.getElementById("dev").textContent);
function fetchTPH(){
  $.ajax({
    url: '/dashboard/' + id + '/' + deviceId + '/charts/1/tph',
    method: 'GET',
    dataType: 'json',
    success: function(data){
      graphTPH(data.temperature_data, data.humidity_data, data.pressure_data, data.labels);
      labelIndex = data.labels.length -1
      dateHolderTPH.old= data.labels[labelIndex]
    },
    error: function(error){
      console.error('Error fetching data: ', error);
    }
  });
}
fetchTPH();
// checks for change in date
function updateTPHByTimeRange(time){
  $.ajax({
    url: '/dashboard/' + id + '/' + deviceId + '/charts/'+ time +'/tph',
    method: 'GET',
    dataType: 'json',
    success: function(data){
      graphTPH(data.temperature_data, data.humidity_data, data.pressure_data, data.labels, time);
      labelIndex = data.labels.length -1
      dateHolderTPH.old= data.labels[labelIndex]
    },
    error: function(error){
      console.error('Error fetching data: ', error);
    }
  });
}
function getLatestTPH(){
  $.ajax({
    url: '/dashboard/' + id + '/' + deviceId + '/charts/tph/latest',
    method: 'GET',
    dataType: 'json',
    success: function(data){
      if(dateDiff(dateHolderTPH.old, data.date_added)){
        updateChart(data.temperature, data.humidity, data.pressure, data.date_added);
        dateHolderTPH.old = data.date_added
      }
    },
    error: function(error){
      console.error('Error getting data: ', error);
    }
  });
}
getLatestTPH();

setInterval(getLatestTPH,3000);


