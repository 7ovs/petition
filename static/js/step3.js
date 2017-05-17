var time_nodes = ['#breakfast', '#lunch', '#dinner']

time_nodes.forEach(function(id){
	$(document).ready(function(){
	    $(id).timepicker({});
	});
})

$(document).ready(function(){
    $('#breakfast').timepicker({
    	timeFormat: 'h:mm p',
    	minTime: '7:00am',
	    maxTime: '12:00am',
    });
});

$(document).ready(function(){
    $('#lunch').timepicker({
    	timeFormat: 'h:mm p',
    	minTime: '13:00pm',
	    maxTime: '17:00pm',
    });
});


$(document).ready(function(){
    $('#dinner').timepicker({
    	timeFormat: 'h:mm p',
    	minTime: '18:00pm',
	    maxTime: '21:00pm',
    });
});