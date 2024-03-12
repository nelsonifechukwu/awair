  const myPopoverTrigger = document.getElementById('popover');
  function getChart(ident){
    $.ajax({
      url: '/analytics/' + id + '/' + deviceId + '/hourly?'+ident,
      method: 'GET',
      dataType: 'json',
      success: function(data){
        console.log(data);
      },
      error: function(error){
  console.error('Error getting data: ', error);
      }
    });
  }
  let hourChart = null;
  const sourceCanvasId = 'hourly-chart';
  let newCanvasId = sourceCanvasId;
  let suffix = 0;
  const instance = new mdb.Popover(myPopoverTrigger, {
      title: "Hourly Forecast",
      sanitize: false,
      html: true,
      template:'<div class="popover" role="tooltip"><div class="arrow"></div><span class="btn btn-link float-right" id="pop-close">x</span><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
      content: () => {
          const html = document.querySelector('#popover-content').innerHTML;
          do{
              suffix += 1;
              newCanvasId = sourceCanvasId + '-' + suffix;
          }while(document.getElementById(newCanvasId));
          // now we have a free id:
          return html.replace(sourceCanvasId, newCanvasId);
      }
  });
 
  myPopoverTrigger.addEventListener('shown.mdb.popover', () => {
    
    close = document.getElementById("pop-close");
    close.addEventListener("click", () => {
        // console.log("Yeah");
        instance.hide();
    });
      const ctxHour = document.getElementById(newCanvasId);
      if (hourChart) {
          hourChart.destroy();
      }
      const hourData = {
        labels:[],
        datasets:[]
      };
      hourChart = new Chart(ctxHour, {
          type: 'line',
          data: hourData,
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
        const ForecastHour = {
        label: "Forecast Temperature",
        data: data.data,
        borderColor: "blue",
        borderWidth: 0.85,
        pointRadius:0,
        fill:true
        };
        
        if(data){
          // console.log(data.data);
          // console.log(data.date);
          
          hourChart.data.labels = data.date ;
          hourChart.data.datasets[0] = ForecastHour;
          hourChart.options.plugins.annotation.annotations.line1.xMin = data.date[0];
          hourChart.options.plugins.annotation.annotations.line1.xMax = data.now;
          hourChart.update(); 
          
        }
        
        }
        
        function getNowChart(){
          $.ajax({
            url: '/analytics/' + id + '/' + deviceId + '/hourly?1',
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
  myPopoverTrigger.addEventListener('hide.mdb.popover', () => {
      if (hourChart) {
          hourChart.destroy();
      }

  });


  


// var url = '/analytics/' + id + '/' + deviceId + '/hourly';
// console.log(url);


