const baseUrl = 'https://s3.amazonaws.com/labelprinter.aaronbeekay.info/label-printer/';
var barcodeField = document.getElementById("variant-barcode");
if(barcodeField){
	var barcode = barcodeField.value;
}

var titleField = document.getElementById("product-name");
if(titleField){
	var title = titleField.value;
} else {
	titleField = document.querySelector("a.ui-breadcrumb > span.ui-breadcrumb__item");
	if(titleField){
		var title = titleField.innerHTML;
	} else {
		var title = '';
	}
}

var conditionField = document.getElementById("variant_option1");
if(conditionField){
	var condition = conditionField.value;
}
qty = window.prompt(`Ready to print: ${title} (${condition}) - barcode ${barcode}... \nHow many?`,0);
if(qty){
	qty = Number(qty);
	var uri = `${baseUrl}pl.html?title=${title}&desc=${condition}&barcode=${barcode}&qty=${qty}&right=now&die=yes`;
	if(qty > 0 && qty < 15){
		console.log(`Printing ${qty} labels (${barcode}) for ${title}`);
		window.open(uri,'_blank','toolbar=0,location=0,menubar=0,height=200,width=200');
	}
	
}