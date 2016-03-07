// Copyright (c) 2016, seethersan and contributors
// For license information, please see license.txt

frappe.provide("ple.libro_electronico_diario");

frappe.ui.form.on('Libro Electronico Diario', {
	refresh: function(frm) {

	}
});
frappe.ui.form.on('Libro Electronico Diario', 'year', function(frm) {
	ple.libro_electronico_diario.check_mandatory_to_set_button(frm);
	
});
frappe.ui.form.on('Libro Electronico Diario', 'periodo', function(frm) {
	ple.libro_electronico_diario.check_mandatory_to_set_button(frm);
	
});
frappe.ui.form.on('Libro Electronico Diario', 'ruc', function(frm) {
	ple.libro_electronico_diario.check_mandatory_to_set_button(frm);
	
});
frappe.ui.form.on('Libro Electronico Diario', 'company', function(frm) {
	frappe.call({
		 	"method": "frappe.client.get",
            args: {
                doctype: "Company",
                name: frm.doc.company
            },
            callback: function (data) {
                if (data.message.company == null) {
                    
                }
                else{
                	frappe.model.set_value(frm.doctype, frm.docname, "ruc", data.message.tax_id);
                }
            }
        });
	ple.libro_electronico_diario.check_mandatory_to_set_button(frm,cdt,cdn);
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
	$.each(["year"], function(i, field) {
		if(!doc[frappe.model.scrub(field)]) frappe.throw(__("Please select {0} first", [field]));
	});
}
frappe.ui.form.on("Libro Electronico Diario", "get_data", function(frm) {
	ple.libro_electronico_diario.check_mandatory_to_fetch(frm.doc);
	$(location).attr('href', "/api/method/ple.ple_peru.doctype.libro_electronico_diario.libro_electronico_diario.export_libro_diario?"+
		"periodo="+frm.doc.periodo+
		"&ruc="+frm.doc.ruc+
		"&year="+frm.doc.year+
		"&primer="+frm.doc.primer_libro);
});
