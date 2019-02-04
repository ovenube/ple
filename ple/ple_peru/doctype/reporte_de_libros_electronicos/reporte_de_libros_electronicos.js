// Copyright (c) 2016, seethersan and contributors
// For license information, please see license.txt
frappe.provide("ple.reporte_de_libros_electronicos");

cur_frm.add_fetch('company', 'tax_id', 'ruc');

frappe.ui.form.on('Reporte de Libros Electronicos', {
	refresh: function(frm) {

	}
});
frappe.ui.form.on('Reporte de Libros Electronicos', 'tipo_libro', function(frm) {
	ple.reporte_de_libros_electronicos.check_mandatory_to_set_button(frm);
	
	
});
frappe.ui.form.on('Reporte de Libros Electronicos', 'year', function(frm) {
	ple.reporte_de_libros_electronicos.check_mandatory_to_set_button(frm);
	
	
});
frappe.ui.form.on('Reporte de Libros Electronicos', 'periodo', function(frm) {
	ple.reporte_de_libros_electronicos.check_mandatory_to_set_button(frm);
	
	
});
frappe.ui.form.on('Reporte de Libros Electronicos', 'ruc', function(frm) {
	ple.reporte_de_libros_electronicos.check_mandatory_to_set_button(frm);
	
	
});
frappe.ui.form.on('Reporte de Libros Electronicos', 'company', function(frm) {
	ple.reporte_de_libros_electronicos.check_mandatory_to_set_button(frm);
	
});
ple.reporte_de_libros_electronicos.check_mandatory_to_set_button = function(frm) {
	if (frm.doc.periodo && frm.doc.ruc && frm.doc.year && frm.doc.tipo_libro) {
		frm.fields_dict.get_data.$input.addClass("btn-primary");
	}
	else{
		frm.fields_dict.get_data.$input.removeClass("btn-primary");
	}
}
ple.reporte_de_libros_electronicos.check_mandatory_to_fetch = function(doc) {
	$.each(["year"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
	$.each(["periodo"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
	$.each(["company"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
	$.each(["ruc"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
	$.each(["tipo_libro"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
}
frappe.ui.form.on("Reporte de Libros Electronicos", "get_data", function(frm) {
	ple.reporte_de_libros_electronicos.check_mandatory_to_fetch(frm.doc);
	frappe.call({
		method: "make_report",
		doc: frm.doc,
		args: {
			'periodo': frm.doc.periodo,
			'tipo': frm.doc.tipo_libro,
			'year': frm.doc.year
		}
	});
});