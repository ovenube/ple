# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "PLE",
			"category": "Modules",
			"label": _("PLE PERU"),
			"color": "#3498db",
			"icon": "octicon octicon-repo",
			"type": "module",
			"description": "Programa de Libros Electronicos"
		}
	]
