var humChart = null;
const humTrigger = document.getElementById('hum-popper');
var humcount=1;
const sourceCan = 'hum-chart';
  let newCan= sourceCan;
  let suff = 0;
const humInstance = new mdb.Popover(humTrigger, {
    title: "Humidity Forecast",
    sanitize: false,
    html: true,
    template:'<div class="popover" role="tooltip"><div class="arrow"></div><span class="btn btn-link float-right" id="pop-closeh">x</span><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
    content: () => {
        const html = document.querySelector('#hum-content').innerHTML;
          do{
              suff += 1;
              newCan = sourceCan + '-' + suff;
          }while(document.getElementById(newCan));
          // now we have a free id:
          return html.replace(sourceCan, newCan);
    }
});
humTrigger.addEventListener('shown.mdb.popover', () => {
    
  
    let close = document.getElementById("pop-closeh");
    close.addEventListener("click", () => {
        // console.log("Yeah");
        humInstance.hide();
    });
      const ctxhum = document.getElementById(newCan);
      if (humChart) {
          humChart.destroy();
      }
      const humData = {
        labels:[],
        datasets:[]
      };
      humChart = new Chart(ctxhum, {
          type: 'line',
          data: humData,
            options: {
              responsive: true,
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
                  annotation: {
                    annotations: {
                      line1: {
                        type: 'box',
                        xMin:'2020-01-01 00:00:00',
                        xMax: '2020-01-01 00:00:00',
                        backgroundColor: 'rgba(0,0,0,0.4)'
                      }
                    }
                  }
                }
            
            }
      });
      function plotNowChart(data){
        const Forecasthum = {
        label: "Forecast hum",
        data: data.data,
        borderColor: "red",
        borderWidth: 0.85,
        pointRadius:0,
        fill:true
        };
        
        if(data){
          // console.log(data.data);
          // console.log(data.date);
          
          humChart.data.labels = data.date ;
          humChart.data.datasets[0] = Forecasthum;
          if(counter==1){
          humChart.options.plugins.annotation.annotations.line1.xMin = data.date[0];
          humChart.options.plugins.annotation.annotations.line1.xMax = data.now;
        }
        else{
          humChart.options.plugins.annotation.annotations.line1.display = false;
        }
          humChart.update(); 
          
        }
        
        }
        
        
        function getNowChart(){
          $.ajax({
            url: '/analytics/' + id + '/' + deviceId + '/hum?'+humcount,
            method: 'GET',
            dataType: 'json',
            success: function(data){
              plotNowChart(data);
            },
            error: function(error){
        console.error('Error getting data: ', error);
            }
          });
        }
        getNowChart();
  });
  humTrigger.addEventListener('hide.mdb.popover', () => {
      if (humChart) {
          humChart.destroy();
      }

  });