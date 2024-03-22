// DOn't know what to plot here yet
var dailyChart = null;
const dailyTrigger = document.getElementById('popover2');
var daycount=1;
const dayInstance = new mdb.Popover(dailyTrigger, {
    title: "Daily Forecast",
    sanitize: false,
    html: true,
    template:'<div class="popover" role="tooltip"><div class="arrow"></div><span class="btn btn-link float-right" id="pop-closed">x</span><h3 class="popover-header"></h3><div class="popover-body"></div></div>',
    content: () => {
        const html = document.querySelector('#popover-content2').innerHTML;
        return html;
    }
});

dailyTrigger.addEventListener('shown.mdb.popover', () => {
    
  
    let close = document.getElementById("pop-closed");
    close.addEventListener("click", () => {
        // console.log("Yeah");
        dayInstance.hide();
    });});

// console.log(myButton);

// const popper = tippy(myButton, {
//     placement:'right',
//     trigger:'click',
//     content: popoverContent.innerHTML,
    
//     // appendTo: document.body,
//     // interactive:true,
//     allowHTML: true,
    

// });
// console.log(popper);