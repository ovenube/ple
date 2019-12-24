# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
        {
            "label": _("Libros Electronicos"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Libro Electronico de Compras",
					"onboard": 1,
                },
				{
                    "type": "doctype",
                    "name": "Libro Electronico de Ventas",
					"onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Libro Electronico de Inventario Permanente Valorizado",
					"onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Libro Electronico Diario",
					"onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Libro Electronico Diario Simplificado",
					"onboard": 1,
                },
            ]
        },
        {
            "label": _("Configuracion"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Catalogo de Existencias",
					"onboard": 1,
                },
				{
                    "type": "doctype",
                    "name": "Tipos de Comprobantes",
					"onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Tipos de Documentos de Identidad",
					"onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Tipos de Existencias",
					"onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Tipos de Operaciones",
					"onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Tipos de Pago",
					"onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Unidades de Medida",
					"onboard": 1,
                },
            ]
        },
        {
            "label": _("Reportes"),
            "items": [
                {
					"type": "report",
					"name": "PLE Compras",
					"doctype": "Purchase Invoice",
                    "is_query_report": True
				},
                {
					"type": "report",
					"name": "PLE Ventas",
					"doctype": "Sales Invoice",
                    "is_query_report": True
				},
                {
                    "type": "doctype",
                    "name": "Reporte de Libros Electronicos",
					"onboard": 1,
                },
            ]
        }
    ]
