# -*- coding: utf-8 -*-
# Copyright (c) 2013, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import datetime
from datetime import timedelta

from ple.ple_peru.utils import Utils

class PLEVentas(Utils):
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})

	def get_columns(self):
		columns = [
			{
				"fieldname": "periodo",
				"label": _("Periodo [01]"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "cuo",
				"label": _("CUO [02]"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "correlativo_asiento",
				"label": _("Correlativo Asiento [03]"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"label": _("Fecha Emisión [04]"),
				"fieldtype": "Data",
				"fieldname": "fecha_emision",
				"width": 90
			},
			{
				"label": _("Fecha Cancelación [05]"),
				"fieldtype": "Data",
				"fieldname": "fecha_cancelacion",
				"width": 90
			},
			{
				"label": _("Tipo Comprobante [06]"),
				"fieldtype": "Link",
				"fieldname": "tipo_comprobante",
				"options": "Tipos de Comprobante",
				"width": 100
			},
			{
				"fieldname": "serie_comprobante",
				"label": _("Serie Comprobante [07]"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "numero_comprobante",
				"label": _("Número Comprobante [08]"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "maquina_registradora",
				"label": _("Resumen Diario [09]"),
				"fieldtype": "Data",
				"width": 90
			},
			{
				"label": _("Tipo Documento [10]"),
				"fieldtype": "Link",
				"fieldname": "tipo_documento",
				"options": "Tipos de Documento de Identidad",
				"width": 90
			},
			{
				"fieldname": "numero_documento",
				"label": _("Número Documento [11]"),
				"fieldtype": "Data",
				"width": 100
			},
			{
				"fieldname": "nombre_cliente",
				"label": _("Nombre Cliente [12]"),
				"fieldtype": "Data",
				"width": 250
			},
			{
				"label": _("Valor Exportación [13]"),
				"fieldname": "valor_exportacion",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Base Imponible [14]"),
				"fieldname": "base_imponible",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Descuento Base Imponible [15]"),
				"fieldname": "descuento_base_imponible",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Monto Impuesto [16]"),
				"fieldname": "monto_impuesto",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Descuento Monto Impuesto [17]"),
				"fieldname": "descuento_monto_impuesto",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Monto Exonerado [18]"),
				"fieldname": "monto_exonerado",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Monto Inafecto [19]"),
				"fieldname": "monto_inafecto",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Monto ISC [20]"),
				"fieldname": "monto_isc",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},			
			{
				"label": _("Monto Arroz Pilado [21]"),
				"fieldname": "monto_arroz_pilado",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},				
			{
				"label": _("Impuesto Arroz Pilado [22]"),
				"fieldname": "impuesto_arroz_pilado",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},		
			{
				"label": _("Otros Conceptos [23]"),
				"fieldname": "otros_conceptos",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Monto Total [24]"),
				"fieldname": "monto_total",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"fieldname": "moneda",
				"label": _("Moneda [25]"),
				"fieldtype": "Link",
				"options": "Currency",
				"width": 100
			},
			{
				"label": _("Tipo Cambio [26]"),
				"fieldname": "tipo_cambio",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Fecha Inicial Devolución [27]"),
				"fieldtype": "Data",
				"fieldname": "fecha_inicial_devolucion",
				"width": 90
			},
			{
				"label": _("Tipo Devolución [28]"),
				"fieldtype": "Link",
				"fieldname": "tipo_devolucion",
				"options": "Tipos de Comprobante",
				"width": 90
			},	
			{
				"fieldname": "serie_devolucion",
				"label": _("Serie Devolución [29]"),
				"fieldtype": "Data",
				"width": 90
			},
			{
				"fieldname": "numero_devolucion",
				"label": _("Número Devolución [30]"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "contrato",
				"label": _("Contrato [31]"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "error_1",
				"label": _("Error 1 [32]"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "indicador_pago",
				"label": _("Indicador Pago [33]"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "estado",
				"label": _("estado [34]"),
				"fieldtype": "Data",
				"width": 120
			}]
		return columns

	def get_data(self):
		sales_invoices = self.get_sales_invoices()
		data = []
		for d in sales_invoices:
			data.append({
				'periodo': d.periodo,
				'cuo': d.cuo,
				'correlativo_asiento': d.correlativo_asiento,
				'fecha_emision': d.fecha_emision,
				'fecha_cancelacion': d.fecha_cancelacion,
				'tipo_comprobante': d.tipo_comprobante,
				'serie_comprobante': d.serie_comprobante,
				'numero_comprobante': d.numero_comprobante,
				'maquina_registradora': d.maquina_registradora,
				'tipo_documento': d.tipo_documento,
				'numero_documento': d.numero_documento,
				'nombre_cliente': d.nombre_cliente,
				'base_imponible_exportacion': d.valor_exportacion,
				'base_imponible': d.base_imponible,
				'descuento_base_imponible': d.descuento_base_imponible,
				'monto_impuesto': d.monto_impuesto,
				'descuento_monto_impuesto': d.descuento_monto_impuesto,
				'monto_exonerado': d.monto_exonerado,
				'monto_inafecto': d.monto_inafecto,
				'monto_isc': d.monto_isc,
				'monto_arroz_pilado': d.monto_arroz_pilado,
				'impuesto_arroz_pilado': d.impuesto_arroz_pilado,
				'otros_conceptos': d.otros_conceptos,
				'monto_total': d.monto_total,
				'moneda': d.moneda,
				'tipo_cambio': d.tipo_cambio,
				'fecha_inicial_devolucion': d.fecha_inicial_devolucion,
				'tipo_devolucion': d.tipo_devolucion,
				'serie_devolucion': d.serie_devolucion,
				'numero_devolucion': d.numero_devolucion,
				'contrato': d.contrato,
				'error_1': d.error_1,
				'indicador_pago': d.indicador_pago,
				'estado': d.estado
				})
		return data

	def run(self):
		columns = self.get_columns()
		data = self.get_data()
		return columns, data

	def get_sales_invoices(self):
		from_date, to_date = self.get_dates(self.filters.year, self.filters.month)
		company = self.filters.company
		sales_invoices = frappe.db.sql("""SELECT
				CONCAT(DATE_FORMAT(posting_date,'%Y%m'),'00') as "periodo",
				REPLACE(sales_invoice.name, '-', '') as "cuo",
				'M1' as "correlativo_asiento",
				DATE_FORMAT(posting_date,'%d/%m/%Y') as "fecha_emision",
				DATE_FORMAT(posting_date,'%d/%m/%Y') as "fecha_cancelacion",
				IF(LENGTH(codigo_comprobante) = 1,CONCAT('0',codigo_comprobante), codigo_comprobante) as "tipo_comprobante",
				SUBSTRING_INDEX(SUBSTRING_INDEX(sales_invoice.name, '-', 2), '-', -1) as "serie_comprobante",
				SUBSTRING_INDEX(sales_invoice.name, '-', -1) as "numero_comprobante",
				"" as "maquina_registradora",
				IF(base_net_total>700,codigo_tipo_documento,IF(ISNULL(tax_id),"",IFNULL(codigo_tipo_documento,""))) as "tipo_documento",
				IF(codigo_tipo_documento=7,IF(SUBSTRING(REPLACE(tax_id,"-",""),-12)="",tax_id, SUBSTRING(REPLACE(tax_id,"-",""),-12)),IF(base_net_total>700,tax_id,IF(ISNULL(tax_id),"",tax_id))) as "numero_documento",
				IF(base_net_total>700,customer_name,IF(ISNULL(tax_id),"",IF(customer_name='Clientes Varios',customer_boleta_name,customer_name))) as "nombre_cliente",
				"" as "valor_exportacion",
				IF(base_total_taxes_and_charges != 0, ROUND(base_net_total, 2), "") as "base_imponible",
				"" as "descuento_base_imponible",
				base_total_taxes_and_charges as "monto_impuesto",
				"" as "descuento_monto_impuesto",
				ROUND(total_amount_free, 2) as "monto_exonerado",
				IF(base_total_taxes_and_charges != 0, "", base_grand_total) as "monto_inafecto",
				"" as "monto_isc",
				"" as "monto_arroz_pilado",
				"" as "impuesto_arroz_pilado",	
				"" as "otros_conceptos",		
				base_grand_total as "monto_total",
				IF(currency = 'SOL', 'PEN', currency) as "moneda",
				SUBSTRING(conversion_rate,1,POSITION('.' in conversion_rate)+3) as "tipo_cambio",
				IF(is_return,(SELECT DATE_FORMAT(sales_return.posting_date,'%d/%m/%Y') FROM `tabSales Invoice` as sales_return WHERE sales_return.name=sales_invoice.return_against),"") as "fecha_inicial_devolucion",
				IF(is_return,(SELECT sales_return.codigo_comprobante FROM `tabSales Invoice` as sales_return WHERE sales_return.name=sales_invoice.return_against),"") as "tipo_devolucion",
				IF(is_return,SUBSTRING((SELECT sales_return.name FROM `tabSales Invoice` as sales_return WHERE sales_return.name=sales_invoice.return_against),4,4),"") as "serie_devolucion",
				IF(is_return,SUBSTRING((SELECT sales_return.name FROM `tabSales Invoice` as sales_return WHERE sales_return.name=sales_invoice.return_against),9),"")  as "numero_devolucion",
				"" as "contrato",
				"" as "error_1",
				'1' as "indicador_pago",
				IF(sales_invoice.docstatus='2','2',IF(CONCAT(DATE_FORMAT(posting_date,'%Y-%m'),'-01')>=posting_date,'7','1')) as "estado"
			FROM
				`tabSales Invoice` as sales_invoice
			WHERE posting_date >= '"""+str(from_date)+"""' 
			AND posting_date <= '"""+str(to_date)+"""'
			AND docstatus != 0
			AND company = '"""+company+"""'
			ORDER BY posting_date""", as_dict=True)

		fees = frappe.db.sql("""SELECT
				CONCAT(DATE_FORMAT(IF(is_return, fecha_nota_credito, fecha_comprobante),'%Y%m'),'00') as "periodo",
				REPLACE(fees.name, '-', '') as "cuo",
				'M1' as "correlativo_asiento",
				DATE_FORMAT(IF(is_return, fecha_nota_credito, fecha_comprobante),'%d/%m/%Y') as "fecha_emision",
				DATE_FORMAT(IF(is_return, fecha_nota_credito, fecha_comprobante),'%d/%m/%Y') as "fecha_cancelacion",
				IF(LENGTH(codigo_comprobante) = 1,CONCAT('0',codigo_comprobante), codigo_comprobante) as "tipo_comprobante",
				SUBSTRING_INDEX(SUBSTRING_INDEX(numero_comprobante, '-', 2), '-', -1) as "serie_comprobante",
				SUBSTRING_INDEX(numero_comprobante, '-', -1) as "numero_comprobante",
				"" as "maquina_registradora",
				codigo_tipo_documento as "tipo_documento",
				IF(codigo_tipo_documento=7,IF(SUBSTRING(REPLACE(tax_id,"-",""),-12)="",tax_id, SUBSTRING(REPLACE(tax_id,"-",""),-12)),IF(grand_total>700,tax_id,IF(ISNULL(tax_id),"",tax_id))) as "numero_documento",
				IF(codigo_tipo_documento=6, razon_social, student_name) as "nombre_cliente",
				"" as "valor_exportacion",
				"" as "base_imponible",
				"" as "descuento_base_imponible",
				"" as "monto_impuesto",
				"" as "descuento_monto_impuesto",
				"" as "monto_exonerado",
				ROUND(grand_total, 2) as "monto_inafecto",
				"" as "monto_isc",
				"" as "monto_arroz_pilado",
				"" as "impuesto_arroz_pilado",
				"" as "otros_conceptos",
				ROUND(grand_total, 2) as "monto_total",
				IF(currency = 'SOL', 'PEN', currency) as "moneda",
				"1.000" as "tipo_cambio",
				IF(is_return,fecha_comprobante,"") as "fecha_inicial_devolucion",
				IF(is_return,tipo_nota_credito,"") as "tipo_devolucion",
				IF(is_return,serie_nota_credito,"") as "serie_devolucion",
				IF(is_return,numero_nota_credito,"")  as "numero_devolucion",
				"" as "contrato",
				"" as "error_1",
				'1' as "indicador_pago",
				IF(fees.docstatus='2','2',IF(CONCAT(DATE_FORMAT(fecha_comprobante,'%Y-%m'),'-01')>=fecha_comprobante,'7','1')) as "estado"
			FROM
				`tabFees` as fees
			WHERE fecha_comprobante  >= '""" + str(from_date) + """' 
			AND fecha_comprobante  <= '""" + str(to_date) + """'
            AND docstatus != 0
            AND company = '"""+company+"""'
			ORDER BY fecha_comprobante""", as_dict=True)
			
		sales_invoices += fees

		return sales_invoices

def execute(filters=None):
	columns, data = PLEVentas(filters).run()

	return columns, data
