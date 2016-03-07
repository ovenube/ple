# -*- coding: utf-8 -*-
# Copyright (c) 2015, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from ple.ple_peru.doctype.libro_electronico_de_compras.libro_electronico_de_compras import get_purchase_invoices
from ple.ple_peru.doctype.libro_electronico_de_ventas.libro_electronico_de_ventas import get_sales_invoices
from ple.ple_peru.doctype.libro_electronico_diario.libro_electronico_diario import get_account
from ple.ple_peru.utils import send_csv_to_client

class ReportedeLibrosElectronicos(Document):
	pass

@frappe.whitelist()
def get_data(year, periodo, tipo):
	if tipo=="Ventas":
		return get_sales_invoices(year, periodo)
	elif tipo=="Compras":
		return get_purchase_invoices(year, periodo)
	elif tipo=="Diario":
		return get_account(year, periodo)

@frappe.whitelist()
def export_reporte_libros(year, periodo, ruc, tipo):
	codigo_periodo = ""
	data = get_data(year, periodo, tipo)
	nombre = "Libro Electronico de "+tipo+" - "+codigo_periodo
	send_csv_to_client(data, nombre, tipo)