var pressChart = null;
const pressTrigger = document.getElementById('pressure-popper');
var presscount=1;
const sourceCanvas = 'press-chart';
  let newCanvas= sourceCanvas;
  let suf = 0;
const pressInstance = new mdb.Popover(pressTrigger, {
    title: "Pressure Forecast",
    sanitize: false,
    html: true,
    template:'<div class="popover" role="tooltip"><div class="arrow"></div><span class="btn btn-link float-right" id="pop-closep">x</span><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
    content: () => {
        const html = document.querySelector('#pressure-content').innerHTML;
          do{
              suf += 1;
              newCanvas = sourceCanvas + '-' + suf;
          }while(document.getElementById(newCanvas));
          // now we have a free id:
          return html.replace(sourceCanvas, newCanvas);
    }
});

pressTrigger.addEventListener('shown.mdb.popover', () => {
    
  
    let close = document.getElementById("pop-closep");
    close.addEventListener("click", () => {
        // console.log("Yeah");
        pressInstance.hide();
    });
      const ctxPress = document.getElementById(newCanvas);
      if (pressChart) {
          pressChart.destroy();
      }
      const pressData = {
        labels:[],
        datasets:[]
      };
      pressChart = new Chart(ctxPress, {
          type: 'line',
          data: pressData,
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
        const ForecastPress = {
        label: "Forecast Pressure",
        data: data.data,
        borderColor: "red",
        borderWidth: 0.85,
        pointRadius:0,
        fill:true
        };
        
        if(data){
          // console.log(data.data);
          // console.log(data.date);
          
          pressChart.data.labels = data.date ;
          pressChart.data.datasets[0] = ForecastPress;
          if(counter==1){
          pressChart.options.plugins.annotation.annotations.line1.xMin = data.date[0];
          pressChart.options.plugins.annotation.annotations.line1.xMax = data.now;
        }
        else{
          pressChart.options.plugins.annotation.annotations.line1.display = false;
        }
          pressChart.update(); 
          
        }
        
        }
        
        
        function getNowChart(){
          $.ajax({
            url: '/analytics/' + id + '/' + deviceId + '/pressure?'+presscount,
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



  pressTrigger.addEventListener('hide.mdb.popover', () => {
      if (pressChart) {
          pressChart.destroy();
      }

  });
