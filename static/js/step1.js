var time_nodes = ['#time_dep', '#time_arr']

$('#phone').keyup(function(e){
    if (/\w/g.test(this.value)){
        // Filter non-digits from input value.
        this.value = this.value.replace(/\D/g, '');
    }
});


$(document).ready(function(){
    $('#time_dep').timepicker({
    	timeFormat: 'h:mm p',
    	minTime: '7:00am',
	    maxTime: '12:00am',
    });
    $('#time_arr').timepicker({
    	timeFormat: 'h:mm p',
    	minTime: '13:00pm',
	    maxTime: '17:00pm',
    });
});
