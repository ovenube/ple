# -*- coding: utf-8 -*-
# Copyright (c) 2015, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TiposdeComprobante(Document):
	pass

@frappe.whitelist()
def get_tipo_comprobante(customer):
	cliente = frappe.get_doc("Customer", customer)
	if cliente.codigo_tipo_documento == '-' or cliente.codigo_tipo_documento == '1':
		comprobante = frappe.get_doc("Tipos de Comprobante", "Boleta de Venta")
	elif cliente.codigo_tipo_documento == '6':
		comprobante = frappe.get_doc("Tipos de Comprobante", "Factura")
	resultado = {"codigo": comprobante.codigo_tipo_comprobante, "descripcion": comprobante.name}
	return resultado
