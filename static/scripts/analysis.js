

console.log("connected")

userData =  {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [{
        label: 'My First dataset',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: [0, 10, 5, 2, 20, 30, 45]
    }]
};
let ctx = document.getElementById('income-chart').getContext('2d');
let chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: userData,

    // Configuration options go here
    options: {}
});


$(document).ready(()=>{
    $('#update').on('click', ()=>{
        userData.datasets[0].data[0]= 100;
        chart.update()
    });

});