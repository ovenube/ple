// Copyright (c) 2016, seethersan and contributors
// For license information, please see license.txt
frappe.provide("ple.libro_electronico_de_compras");

frappe.ui.form.on('Libro Electronico de Compras', {
	refresh: function(frm) {

	}
});
frappe.ui.form.on('Libro Electronico de Compras', 'periodo', function(frm) {
	ple.libro_electronico_de_compras.check_mandatory_to_set_button(frm);
	
	
});
frappe.ui.form.on('Libro Electronico de Compras', 'ruc', function(frm) {
	ple.libro_electronico_de_compras.check_mandatory_to_set_button(frm);
	
	
});
frappe.ui.form.on('Libro Electronico de Compras', 'company', function(frm) {
	ple.libro_electronico_de_compras.check_mandatory_to_set_button(frm);
	if (frm.doc.company) {frm.doc.ruc = null};
	
	
});
ple.libro_electronico_de_compras.check_mandatory_to_set_button = function(frm) {
	if (frm.doc.periodo && frm.doc.ruc) {
		frm.fields_dict.get_data.$input.addClass("btn-primary");
	}
	else{
		frm.fields_dict.get_data.$input.removeClass("btn-primary");
	}
}
ple.libro_electronico_de_compras.check_mandatory_to_fetch = function(doc) {
	$.each(["periodo"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
	$.each(["company"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
}
frappe.ui.form.on("Libro Electronico de Compras", "get_data", function(frm) {
	ple.libro_electronico_de_compras.check_mandatory_to_fetch(frm.doc);
	$(location).attr('href', "/api/method/ple.ple_peru.doctype.libro_electronico_de_compras.libro_electronico_de_compras.export_libro_de_compras?"+
		"periodo="+frm.doc.periodo+
		"&ruc="+frm.doc.ruc);
});
