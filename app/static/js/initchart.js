// Reusable function for chart initialization and data fetching
var count = 1;
let activeInstance = null;
var num = JSON.parse(document.getElementById("num").textContent);
function initializeChart(triggerId, contentId, dataUrl, chartType, chartLabel, color) {
    let chart = null;
    const sourceCanvas = `${chartType}-chart`;
    let newCanvas = sourceCanvas;
    let suf = 0;

    const trigger = document.getElementById(triggerId);
    const instance = new mdb.Popover(trigger, {
        title: `${chartLabel} Forecast`,
        sanitize: false,
        html: true,
        template: `
            <div class="popover" role="tooltip">
                <div class="arrow"></div>
                <span class="btn btn-link float-right" id="pop-close-${chartType}">x</span>
                <h3 class="popover-header"></h3>
                <div class="popover-body"></div>
            </div>
        `,
        content: () => {
            const html = document.querySelector(`#${contentId}`).innerHTML;
            do {
                suf += 1;
                newCanvas = `${sourceCanvas}-${suf}`;
            } while (document.getElementById(newCanvas));
            return html.replace(sourceCanvas, newCanvas);
        }
    });
    
trigger.addEventListener('show.mdb.popover', ()=>{
    if (activeInstance && activeInstance !== instance) {
        activeInstance.hide();
    }
    activeInstance = instance;

});
    trigger.addEventListener('shown.mdb.popover', () => {
        
       
        const close = document.getElementById(`pop-close-${chartType}`);
        close.addEventListener('click', () => {
            activeInstance.hide();
        });

        const ctx = document.getElementById(newCanvas);
        if (chart) {
            chart.destroy();
        }
        const dataObject = {
            labels: [],
            datasets: []
        };
        chart = new Chart(ctx, {
            type: 'line',
            data: dataObject,
            options: {
                responsive: true,
                // tooltips: {
                //     mode: 'nearest',
                //     intersect: true
                // },
                // interaction: {
                //     intersect: false
                // },
                
    
                scales: {
                    x: {
                        ticks:{
                            color:"white",
                        },
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
                        ticks:{
                            color:"white",
                        },
                        title: {
                            display: false,
                            text: '(0c, Kpa, %)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: "white",
                            
                        }
                    },
                    tooltip: {
                        callbacks: {
                          label: function (context) {
                            const label = context.dataset.label || '';
                            if (label && chartType=='wind') {
                              return `${label}: ${context.formattedValue} \n Wind Direction:${context.dataset.rotation[context.dataIndex]}`;
                            }
                            return context.formattedValue;
                          }
                        }
                  
                      },
                    annotation: {
                        annotations: {
                            line1: {
                                type: 'box',
                                xMin: '2020-01-01 00:00:00',
                                xMax: '2020-01-01 00:00:00',
                                backgroundColor: '#7d94b3a5',
                                borderWidth: 0
                
                            }
                        }
                    }
                }
            }
        });

        function plotChart(data) {
            var customImage = new Image(10, 12);
  customImage.src = '/static/assets/arrow_up_thick.png';
                   const windData = {
                      label: `${chartLabel}`,
                      data: data.data.map(entry => entry.speed),
                      borderColor: 'grey',
                      borderWidth: 1,
                
                      fill: true,
                      pointStyle: customImage,
                      rotation: data.data.map(entry => entry.direction),
                      pointRadius: 18,
                      cubicInterpolationMode: 'monotone',
                      tension: 0.4
                    }
                
             
            
            const forecastData = {
                label: `Forecast ${chartLabel}`,
                data: data.data,
                borderColor: `${color}`,
                borderWidth: 1.3,
                pointRadius: 0,
                fill: true
            };

            if (data) {
                chart.data.labels = data.date;
                if(chartType == 'wind'){
                    // console.log(windData);
                    chart.data.datasets[0] = windData;  
                }
                else{ 
                    chart.data.datasets[0] = forecastData;
                }
               
                if (count == 1) {
                    chart.options.plugins.annotation.annotations.line1.xMin = data.date[0];
                    chart.options.plugins.annotation.annotations.line1.xMax = data.now;
                } else {
                    chart.options.plugins.annotation.annotations.line1.display = false;
                }
                chart.update();
            }
        }

        function fetchData() {
            $.ajax({
                url: dataUrl + count,
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    plotChart(data);
                    
                },
                error: function(error) {
                    console.error('Error getting data: ', error);
                }
            });
        }
        fetchData();
    });

    trigger.addEventListener('hide.mdb.popover', () => {
        if (chart) {
            chart.destroy();
        }
    });
    // return instance;
}
// Initialize Hour Chart
initializeChart('popover', 'popover-content','/analytics/' + id + '/' + deviceId + '/hourly?temp,', 'hourly', 'Hourly', 'blue');
// Initialize Pressure Chart
initializeChart('pressure-popper', 'pressure-content', '/analytics/' + id + '/' + deviceId + '/hourly?pressure,', 'press', 'Pressure','red');

// Initialize Humidity Chart
initializeChart('hum-popper', 'hum-content', '/analytics/' + id + '/' + deviceId + '/hourly?hum,', 'hum', 'Humidity','green');
// Initialize Feels Like Chart
initializeChart('feel-popper','feel-content','/analytics/' + id + '/' + deviceId + '/hourly?feel,', 'feel', 'Feels Like', 'orange');

// Initialize Rain Chart
initializeChart('rain-popper', 'rain-content', '/analytics/' + id + '/' + deviceId + '/hourly?rain,', 'rain', 'Rain Amount', 'blue');
// Initialize Wind Chart
initializeChart('wind-popper', 'wind-content', '/analytics/' + id + '/' + deviceId + '/hourly?wind,', 'wind', 'Wind Speed', 'blue');

function getChart(ident,time){
    $.ajax({
      url: '/analytics/' + id + '/' + deviceId + '/check?'+ident,
      method: 'GET',
      dataType: 'json',
      success: function(data){
        dataChange(data, ident,time);
      },
      error: function(error){
        console.error('Error getting data: ', error);
      }
    });
  }

function dataChange(data, ident,time){
  const ddate = document.getElementById(time);
  const todayDay = document.querySelectorAll('.circle');
  todayDay.forEach(element => {
      element.classList.remove('circle');
  });
  const sp = document.getElementById(ident);
  sp.querySelector('span').classList.add('circle')
  ddate.innerText = data.date;
        count = ident;
        activeInstance.show();
}
function getNext(d, time){
    if(d=='n'){
        if(count<num){
          count+=1; }
        
      }
      else{
        if(count>1){
        count-=1;}
        else{
          count=1;
        }
      }   
        getChart(count, time);
    }