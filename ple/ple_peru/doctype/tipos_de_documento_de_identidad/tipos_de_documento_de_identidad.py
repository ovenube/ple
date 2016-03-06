# -*- coding: utf-8 -*-
# Copyright (c) 2015, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TiposdeDocumentodeIdentidad(Document):
	pass

@frappe.whitelist()
def get_tipo_documento(tipo_documento_identidad):
	tipo_documento = frappe.get_doc("Tipos de Documento de Identidad", tipo_documento_identidad)
	return tipo_documento.codigo_tipo_documento