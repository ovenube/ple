# -*- coding: utf-8 -*-
# Copyright (c) 2015, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TiposdeComprobante(Document):
	pass

@frappe.whitelist()
def get_tipo_comprobante(tipo_comprobante):
	comprobante = frappe.get_doc("Tipos de Comprobante", tipo_comprobante)
	resultado = {"nombre": comprobante.codigo_tipo_comprobante, "descripcion": " ".join(filter(None,[comprobante.descripcion_tipo_comprobante]))}
	return resultado
