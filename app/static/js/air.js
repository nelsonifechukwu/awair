// Air Quality graph
const ctx3 = document.getElementById('air');
function graphAir(pmtwo_data, pmten_data, co_data, labels, time='1'){
  const pmtwoData = {
    label: "pmtwo (μg/m3)",
    data: pmtwo_data,
    borderColor: "red",
    borderWidth: 0.85,
    pointRadius: 0,
    fill: false,
    // I am using stepped before(Might change this later) and fill false: Might change for other kinds of data
    // stepped: true,
    // for curvature of line
    // cubicInterpolationMode: 'monotone',
    // tension:0.4,
  };
  const pmtenData = {
    label: "pmten (μg/m3)",
    data: pmten_data,
    borderColor: "orange",
    borderWidth: 0.85,
    pointRadius: 0,
    fill: false,
    // stepped: true,
    // cubicInterpolationMode: 'monotone',
    // tension: 0.4,
  };
  const coData = {
    label: 'co (ppm)',
    data: co_data,
    borderColor: 'grey',
    borderWidth: 0.85,
    pointRadius: 0,
    fill: false,
    // stepped: true,
    // cubicInterpolationMode: 'monotone',
    // tension: 0.4,
  };
  if(time=='1'){
    air.options.scales.x.time.unit = 'hour';
  }
  else if(time == '7'){
    air.options.scales.x.time.unit = 'day';
  }
  else if(time == '4'){
    air.options.scales.x.time.unit = 'month';
  }
  else if(time == '52'){
    air.options.scales.x.time.unit = 'year';
  }
  air.data.labels = labels;
  air.data.datasets[0] = pmtwoData;
  air.data.datasets[1] = pmtenData;
  air.data.datasets[2] = coData;
  air.update();
};


const airData = {
  labels: [],
  datasets: []
};

const option3 = {
  responsive: true,
  maintainAspectRatio: false,
  title: {
display: true,
text: "Air Quality data"
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
        text: '(μg/m3)'
      }
    }
  },
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Air Quality'
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



const air = new Chart(ctx3, {
  type: 'line',
  
  data:airData,
  options:option3
  
});
// Date Difference
const dateHolderAir = {
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
function updateAirChart(pmtwo_data, pmten_data, co_data, labels){
  air.data.labels.push(labels);
  
  air.data.datasets[0].data.push(pmtwo_data);
  air.data.datasets[1].data.push(pmten_data);
  air.data.datasets[2].data.push(co_data);
  air.update();
  

}

// Ajax
var id = JSON.parse(document.getElementById("id").textContent);
var deviceId = JSON.parse(document.getElementById("dev").textContent);
function fetchAir(){
  $.ajax({
    url: '/dashboard/' + id + '/' + deviceId + '/charts/1/air',
    method: 'GET',
    dataType: 'json',
    success: function(data){
      graphAir(data.pmtwo_data, data.pmten_data, data.co_data, data.labels);
      labelIndex = data.labels.length -1
      dateHolderAir.old= data.labels[labelIndex]
    },
    error: function(error){
      console.error('Error fetching data: ', error);
    }
  });
}
fetchAir();
// checks for change in date
function updateAirByTimeRange(time){
  $.ajax({
    url: '/dashboard/' + id + '/' + deviceId + '/charts/'+ time +'/air',
    method: 'GET',
    dataType: 'json',
    success: function(data){
      graphAir(data.pmtwo_data, data.pmten_data, data.co_data, data.labels, time);
      labelIndex = data.labels.length -1
      dateHolderAir.old= data.labels[labelIndex]
    },
    error: function(error){
      console.error('Error fetching data: ', error);
    }
  });
}
function getLatestAir(){
  $.ajax({
    url: '/dashboard/' + id + '/' + deviceId + '/charts/air/latest',
    method: 'GET',
    dataType: 'json',
    success: function(data){
      if(dateDiff(dateHolderAir.old, data.date_added)){
        updateAirChart(data.pmtwo, data.pmten, data.co, data.date_added);
        dateHolderAir.old = data.date_added
      }
    },
    error: function(error){
      console.error('Error getting data: ', error);
    }
  });
}
getLatestAir();

setInterval(getLatestAir,3000);
