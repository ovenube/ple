// Copyright (c) 2018, seethersan and contributors
// For license information, please see license.txt

frappe.provide("ple.libro_electronico_mayor");

cur_frm.add_fetch('company', 'tax_id', 'ruc');

frappe.ui.form.on('Libro Electronico Mayor', {
	refresh: function(frm) {

	}
});

frappe.ui.form.on('Libro Electronico Mayor', 'year', function(frm) {
	ple.libro_electronico_mayor.check_mandatory_to_set_button(frm);
	
});

frappe.ui.form.on('Libro Electronico Mayor', 'periodo', function(frm) {
	ple.libro_electronico_mayor.check_mandatory_to_set_button(frm);
	
});

frappe.ui.form.on('Libro Electronico Mayor', 'ruc', function(frm) {
	ple.libro_electronico_mayor.check_mandatory_to_set_button(frm);
	
});

frappe.ui.form.on('Libro Electronico Mayor', 'company', function(frm, cdt, cdn) {
	ple.libro_electronico_mayor.check_mandatory_to_set_button(frm, cdt, cdn);
});

ple.libro_electronico_mayor.check_mandatory_to_set_button = function(frm) {
	if (frm.doc.periodo && frm.doc.ruc) {
		frm.fields_dict.get_data.$input.addClass("btn-primary");
	}
	else{
		frm.fields_dict.get_data.$input.removeClass("btn-primary");
	}
};

ple.libro_electronico_mayor.check_mandatory_to_fetch = function(doc) {
	$.each(["periodo"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
	$.each(["company"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
	$.each(["year"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
};

frappe.ui.form.on("Libro Electronico Mayor", "get_data", function(frm) {
	ple.libro_electronico_mayor.check_mandatory_to_fetch(frm.doc);
	frappe.call({
		method: "export_libro_mayor",
		doc: frm.doc,
		args: {
			'company': frm.doc.company,
			'periodo': frm.doc.periodo,
			'ruc': frm.doc.ruc,
			'year': frm.doc.year
		},
		callback: function (r){
			if (r.message){
				$(location).attr('href', "/api/method/ple.ple_peru.utils.send_file_to_client?"+
				"file="+r.message.archivo+
				"&tipo="+r.message.tipo+
				"&nombre="+r.message.nombre);
			}
		}
	});
});
