# -*- coding: utf-8 -*-
# Copyright (c) 2015, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TiposdePago(Document):
	pass

@frappe.whitelist()
def get_tipo_pago(tipo_pago):
	pago = frappe.get_doc("Tipos de Pago", tipo_pago)
	return pago.codigo_tipo_pago
