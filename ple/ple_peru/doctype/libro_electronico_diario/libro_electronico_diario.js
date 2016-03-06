// Copyright (c) 2016, seethersan and contributors
// For license information, please see license.txt

frappe.provide("ple.libro_electronico_diario");

frappe.ui.form.on('Libro Electronico Diario', {
	refresh: function(frm) {

	}
});
frappe.ui.form.on('Libro Electronico Diario', 'periodo', function(frm) {
	ple.libro_electronico_diario.check_mandatory_to_set_button(frm);
	
});
frappe.ui.form.on('Libro Electronico Diario', 'ruc', function(frm) {
	ple.libro_electronico_diario.check_mandatory_to_set_button(frm);
	
});
frappe.ui.form.on('Libro Electronico Diario', 'company', function(frm) {
	ple.libro_electronico_diario.check_mandatory_to_set_button(frm);
	if (frm.doc.company) {frm.doc.ruc = null};
	
});
ple.libro_electronico_diario.check_mandatory_to_set_button = function(frm) {
	if (frm.doc.periodo && frm.doc.ruc) {
		frm.fields_dict.get_data.$input.addClass("btn-primary");
	}
	else{
		frm.fields_dict.get_data.$input.removeClass("btn-primary");
	}
}
ple.libro_electronico_diario.check_mandatory_to_fetch = function(doc) {
	$.each(["periodo"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
	$.each(["company"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
}
frappe.ui.form.on("Libro Electronico Diario", "get_data", function(frm) {
	ple.libro_electronico_diario.check_mandatory_to_fetch(frm.doc);
	$(location).attr('href', "/api/method/ple.ple_peru.doctype.libro_electronico_diario.libro_electronico_diario.export_libro_diario?"+
		"periodo="+frm.doc.periodo+
		"&ruc="+frm.doc.ruc+
		"&primer="+frm.doc.primer_libro);
});
