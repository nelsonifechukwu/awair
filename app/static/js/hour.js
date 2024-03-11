const labelScroll ={};
const dataScroll = {};
document.addEventListener('DOMContentLoaded', function() {
  const myPopoverTrigger = document.getElementById('popover');
  let hourChart = null;
  const sourceCanvasId = 'hourly-chart';
  let newCanvasId = sourceCanvasId;
  let suffix = 0;
  const instance = new mdb.Popover(myPopoverTrigger, {
      title: "Hourly Forecast",
      sanitize: false,
      html: true,
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

  myPopoverTrigger.addEventListener('shown.bs.popover', () => {
      const ctxHour = document.getElementById(newCanvasId);
      if (hourChart) {
          hourChart.destroy();
      }
      hourChart = new Chart(ctxHour, {
          type: 'line',
          data: {
              labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
              datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
      });
  });
  myPopoverTrigger.addEventListener('hide.bs.popover', () => {
      if (hourChart) {
          hourChart.destroy();
      }

  });
  
});

