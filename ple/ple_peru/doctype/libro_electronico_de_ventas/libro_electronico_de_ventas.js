// Copyright (c) 2016, seethersan and contributors
// For license information, please see license.txt
frappe.provide("ple.libro_electronico_de_ventas");

frappe.ui.form.on('Libro Electronico de Ventas', {
	refresh: function(frm) {

	}
});
frappe.ui.form.on('Libro Electronico de Ventas', 'periodo', function(frm) {
	ple.libro_electronico_de_ventas.check_mandatory_to_set_button(frm);
	
});
frappe.ui.form.on('Libro Electronico de Ventas', 'ruc', function(frm) {
	ple.libro_electronico_de_ventas.check_mandatory_to_set_button(frm);
	
});
frappe.ui.form.on('Libro Electronico de Ventas', 'company', function(frm) {
	ple.libro_electronico_de_ventas.check_mandatory_to_set_button(frm);
	frappe.call({
		 	"method": "frappe.client.get",
            args: {
                doctype: "Company",
                name: frm.doc.company
            },
            callback: function (data) {
                if (data.message.company_name == null) {
                    
                }
                else{
                	frappe.model.set_value(frm.doctype, frm.docname, "ruc", data.message.tax_id);
                }
            }
        });
	
});
ple.libro_electronico_de_ventas.check_mandatory_to_set_button = function(frm) {
	if (frm.doc.periodo && frm.doc.ruc) {
		frm.fields_dict.get_data.$input.addClass("btn-primary");
	}
	else{
		frm.fields_dict.get_data.$input.removeClass("btn-primary");
	}
}
ple.libro_electronico_de_ventas.check_mandatory_to_fetch = function(doc) {
	$.each(["periodo"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
	$.each(["company"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
}
frappe.ui.form.on("Libro Electronico de Ventas", "get_data", function(frm) {
	ple.libro_electronico_de_ventas.check_mandatory_to_fetch(frm.doc);
	frappe.call({
		method: "export_libro_ventas",
		doc: frm.doc,
		args: {
			'periodo': frm.doc.periodo,
			'ruc': frm.doc.ruc,
			'year': frm.doc.year
		}
	});
});
