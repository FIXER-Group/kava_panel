function getCriticColor(percent) {
	if (percent<50){
	  return "#28a745";
	}
	else if(percent>=50 && percent<90){
		return "#fd7e14";
	}
    else{
		return "#dc3545";
	}
}

	var cpu_circle = Circles.create({
		id:           'cpu',
		radius:       75,
		value:        0,
		maxValue:     100,
		width:        8,
		text:         function(value){return value + '%';},
		colors:       ['#eee', '#1D62F0'],
		duration:     400,
		wrpClass:     'circles-wrp',
		textClass:    'circles-text',
		styleWrapper: true,
		styleText:    true
	});

Circles.create({
	id:           'ram',
	radius:       75,
	value:        50,
	maxValue:     100,
	width:        8,
	text:         function(value){return value + '%';},
	colors:       ['#eee', '#28a745'],
	duration:     400,
	wrpClass:     'circles-wrp',
	textClass:    'circles-text',
	styleWrapper: true,
	styleText:    true
})
Circles.create({
	id:           'disc',
	radius:       75,
	value:        90,
	maxValue:     100,
	width:        8,
	text:         function(value){return value + '%';},
	colors:       ['#eee', '#fd7e14'],
	duration:     400,
	wrpClass:     'circles-wrp',
	textClass:    'circles-text',
	styleWrapper: true,
	styleText:    true
})

$.notify({
	icon: 'las la-check-circle',
	title: 'You have successfully logged in.',
	message: ''
},{
	type: 'success',
	placement: {
		from: "top",
		align: "right"
	},
	time: 900000000,
});

// monthlyChart

Chartist.Pie('#monthlyChart', {
	labels: ['50%', '20%', '30%'],
	series: [50, 20, 30]
}, {
	plugins: [
	Chartist.plugins.tooltip()
	]
});

// trafficChart
var chart = new Chartist.Line('#trafficChart', {
	labels: [1, 2, 3, 4, 5, 6, 7],
	series: [
	[5, 9, 7, 8, 5, 3, 5],
	[6, 9, 5, 10, 2, 3, 7],
	[2, 7, 4, 10, 7, 6, 2]
	]
}, {
	plugins: [
	Chartist.plugins.tooltip()
	],
	low: 0,
	height: "245px",
});

// salesChart
var dataSales = {
	labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
	series: [
	[5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8],
	[3, 2, 9, 5, 4, 6, 4, 6, 7, 8, 7, 4]
	]
}

var optionChartSales = {
	plugins: [
	Chartist.plugins.tooltip()
	],
	seriesBarDistance: 10,
	axisX: {
		showGrid: false
	},
	height: "245px",
}

var responsiveChartSales = [
['screen and (max-width: 640px)', {
	seriesBarDistance: 5,
	axisX: {
		labelInterpolationFnc: function (value) {
			return value[0];
		}
	}
}]
];

Chartist.Bar('#salesChart', dataSales, optionChartSales, responsiveChartSales);
