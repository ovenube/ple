// Copyright (c) 2016, seethersan and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PLE Compras"] = {
	"filters": [
		{
			"fieldname":"month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options": 'Enero\nFebrero\nMarzo\nAbril\nMayo\nJunion\nJulio\nAgosto\nSetiembre\nOctubre\nNoviembre\nDiciembre',
			"default": "Enero"
		},
		{
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Select",
			"options": '2017\n2018\n2019\n2020\n2021\n2022\2023',
			"default": "2019"
		},
	],
	onload: function(report) {
		
	}
}
