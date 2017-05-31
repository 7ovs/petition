var personDivIDs = ['div-children', 'div-сlergy', 'div-brothers', 'div-sisters']

var getCounter = function(){
	var numbers = []
	personDivIDs.forEach(function(div_id){
		var celNumber = getPersonCellNubmer(div_id);
		numbers.push(celNumber)
	});
	console.log(numbers)
	var maxNumber = Math.max.apply(null, numbers)
	console.log(maxNumber)
	return maxNumber
}


var getPersonCellNubmer = function(div_id){
	var parentNode = document.getElementById(div_id);
	var inputNode = parentNode.querySelector("table tbody tr td input");
	if(inputNode){
		return inputNode.id.split(" ")[2]
	}

}

var counter = getCounter();

var addRow = function(btn){
	var table = document.getElementById("table-"+btn.id);
    var row = table.insertRow(-1);
    var nameCell = row.insertCell(0);
    var deleteButton = row.insertCell(1);

    nameCell.innerHTML = "<input name=\""+btn.id+" cell "+counter+"\" id=\""+btn.id+" cell "+counter+"\">";
    deleteButton.innerHTML = "<i class=\"material-icons del_row_button\" onclick=\"deleteRow(this)\" title=\"delete\">clear</i>";
	counter++;
}

var deleteRow = function(btn){
	var cell = btn.parentNode;
	var row = cell.parentNode;
	row.remove();
}
