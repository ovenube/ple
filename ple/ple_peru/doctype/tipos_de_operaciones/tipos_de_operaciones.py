# -*- coding: utf-8 -*-
# Copyright (c) 2018, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TiposdeOperaciones(Document):
	pass

def get_operacion(proposito, stock):
	if proposito == "Manufactura":
		if stock > 0:
			operacion = frappe.get_doc("Tipos de Operaciones", "19")
		else:
			operacion = frappe.get_doc("Tipos de Operaciones", "10")
	elif proposito == "Transferencia de Material":
		if stock > 0:
			operacion = frappe.get_doc("Tipos de Operaciones", "26")
		else:
			operacion = frappe.get_doc("Tipos de Operaciones", "27")
	elif proposito == "Recepción de Materiales":
		operacion = frappe.get_doc("Tipos de Operaciones", "16")
	elif proposito == "Transferencia de Material":
		if stock > 0:
			operacion = frappe.get_doc("Tipos de Operaciones", "21")
		else:
			operacion = frappe.get_doc("Tipos de Operaciones", "11")
	return operacion.codigo_tipos_operacion