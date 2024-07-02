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
		backgroundColor: 'rgb(75, 192, 192)',
		borderColor: 'rgb(75, 192, 192)',
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

$(document).ready(function () {
	// general Doughnut and Line charts
	var labels = [
		'starcodes',
		'markdowns',
		'codelord2345',
		'codexmax21',
		'procode52',
		'others'
	];
	var label = 'Total Commits';
	var data = [12, 19, 3, 5, 2, 3];
	//var genDoughChart = doughnutChart(labels, label, data, $('#genDoughChart'));
	
	const year = [2012, 2013, 2014, 2015, 2016, 2017, 2018];
	data = [12, 19, 3, 5, 2, 3, 10];
	label = 'Total No of Commits';
	var genLineChart = lineChart(year, label, data, $('#genLineChart'));
	
	// Last 7 days Line and Bar charts
	labels = [
		'06/14',
		'06/15',
		'06/16',
		'06/17',
		'06/18',
		'06/19',
		'06/20',
	];
	data = [10, 15, 2, 3, 1, 11, 8];
	label = 'Daily Commits';
	var dailyCommit = lineChart(labels, label, data, $('#dailyCommit'));
	
	data = [[10, 15, 2, 3, 1, 11, 8], [2, 4, 6, 8, 4, 3, 6]];
	label = ['Closed Issues', 'Open Issues'];
	var dailyIssues = barChart(labels, label, data, $('#dailyIssues'));
	
	// Last 8 weeks Line and Bar charts
	labels = [
		'18th',
		'19th',
		'20th',
		'21st',
		'22nd',
		'23rd',
		'24th',
		'25th',
	];
	data = [10, 15, 2, 3, 1, 11, 8, 20];
	label = 'Weekly Commits';
	var weeklyCommit = lineChart(labels, label, data, $('#weeklyCommit'));
	
	data = [[10, 15, 2, 3, 1, 11, 8, 18], [2, 4, 6, 8, 4, 3, 6, 2]];
	label = ['Closed Issues', 'Open Issues'];
	var weeklyIssues = barChart(labels, label, data, $('#weeklyIssues'));
	
	// Last 12 months Line and Bar charts
	labels = [
		'Jan', 'Feb',
		'Mar', 'Apr',
		'May', 'Jun',
		'Jul', 'Aug',
		'Sep', 'Oct',
		'Nov', 'Dec'
	];
	data = [10, 15, 2, 3, 1, 11, 8, 20, 10, 15, 2, 3];
	label = 'Weekly Commits';
	var monthlyCommit = lineChart(labels, label, data, $('#monthlyCommit'));
	
	data = [
		[10, 15, 2, 3, 1, 11, 8, 18, 10, 15, 2, 3],
		[2, 4, 6, 8, 4, 3, 6, 2, 2, 4, 6, 8]
	];
	label = ['Closed Issues', 'Open Issues'];
	var monthlyIssues = barChart(labels, label, data, $('#monthlyIssues'));
  //const note = genLineChart.data.datasets[0].label;
  //console.log(note);
});
