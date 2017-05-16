var i
var persons_integer_only = ['#brothers', '#sisters', '#children', '#clerics']//integer only fields
var date_nodes = ['#date_arr', '#date_dep']

pers_num_summ = function(){ //summ of persons
	function getSum(total, num) {
	    return total + num;
	}
	summ = []
	persons_integer_only.forEach(function(id){
		var quantity = $(id).val()
		quantity = parseInt(quantity)
		if (!quantity){
			quantity = 0
		}
		summ.push(quantity)
	});	
	$('.pers_num').text(summ.reduce(getSum));
}

integer_only = function(id){//prevent not integer input
	$(id).keyup(function(e){
		if (/\D/g.test(this.value)){
			// Filter non-digits from input value.
			this.value = this.value.replace(/\D/g, '');
		}
	});
}

persons_integer_only.forEach(function(id){
	integer_only(id);
	$(id).change(function(e){
		pers_num_summ();
	});
});

nights = function(){// count nights of living
	var arr = $('#date_arr').val()
	var dep = $('#date_dep').val()
	var diffDays
	arr = Date.parse(arr)
	dep = Date.parse(dep)
	if(arr&&dep){
		diffDays = Math.ceil((dep - arr) / (1000 * 3600 * 24)); 
		$('.nights').text(diffDays)
	}
	if (!diffDays){
		$('.nights').text(0)
	}
}

date_nodes.forEach(function(id){
	$(id).change(function(){
		nights()
	});
	$(id).pickadate({
		selectMonths: true, // Creates a dropdown to control month
		selectYears: 15 // Creates a dropdown of 15 years to control year
	});
});


$(document).ready(function(){
	pers_num_summ();
	nights()
})