function doughnutChart(labels, label, data, ctx) {
	const chart = new Chart(ctx, {
		type: 'doughnut',
		data: {
			labels: labels,
			datasets: [{
			label: label,
			data: data,
			backgroundColor: [
			  'rgb(255, 99, 132)',
			  'rgb(255, 159, 64)',
			  'rgb(255, 205, 86)',
			  'rgb(75, 192, 192)',
			  'rgb(54, 162, 235)',
			  'rgb(153, 102, 255)'
			],
			hoverOffset: 4
		  }]
		}
	});
	return chart;
}

function lineChart(labels, label, data, ctx) {
  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: label,
        data: data,
	backgroundColor: 'rgba(75, 192, 192, 0.8)',
        fill: true,
	borderColor: 'rgb(54, 162, 235)',
        borderWidth: 2,
	tension: 0.1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
  
  return chart;
}

function barChart(labels, label, data, ctx) {
  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: label[0],
        data: data[0],
		backgroundColor: 'rgb(75, 192, 192)',
        borderWidth: 1
      },
	  {
        label: label[1],
        data: data[1],
		backgroundColor: 'rgb(255, 159, 64)',
        borderWidth: 0
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
		  stacked: true
        },
		x: {
			stacked: true
		}
      }
    }
  });
  
  return chart;
}
