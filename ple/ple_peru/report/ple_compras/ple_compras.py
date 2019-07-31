# -*- coding: utf-8 -*-
# Copyright (c) 2013, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import datetime
from datetime import timedelta

from ple.ple_peru.utils import Utils

class PLECompras(Utils):
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})

	def get_columns(self):
		columns = [
			{
				"fieldname": "periodo",
				"label": _("Periodo"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "cuo",
				"label": _("CUO"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "correlativo_asiento",
				"label": _("Correlativo Asiento"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"label": _("Fecha Emisión"),
				"fieldtype": "Data",
				"fieldname": "fecha_emision",
				"width": 90
			},
			{
				"label": _("Fecha Cancelación"),
				"fieldtype": "Data",
				"fieldname": "fecha_cancelacion",
				"width": 90
			},
			{
				"label": _("Tipo Comprobante"),
				"fieldtype": "Link",
				"fieldname": "tipo_comprobante",
				"options": "Tipos de Comprobante",
				"width": 100
			},
			{
				"fieldname": "serie_comprobante",
				"label": _("Serie Comprobante"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "codigo_dua",
				"label": _("Código DUA"),
				"fieldtype": "Data",
				"width": 90
			},
			{
				"fieldname": "numero_comprobante",
				"label": _("Número Comprobante"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "resumen_diario",
				"label": _("Resumen Diario"),
				"fieldtype": "Data",
				"width": 90
			},
			{
				"label": _("Tipo Documento"),
				"fieldtype": "Link",
				"fieldname": "tipo_documento",
				"options": "Tipos de Documento de Identidad",
				"width": 90
			},
			{
				"fieldname": "resumen_diario",
				"label": _("Resumen Diario"),
				"fieldtype": "Data",
				"width": 90
			},
			{
				"fieldname": "numero_documento",
				"label": _("Número Documento"),
				"fieldtype": "Data",
				"width": 100
			},
			{
				"fieldname": "nombre_proveedor",
				"label": _("Nombre Proveedor"),
				"fieldtype": "Data",
				"width": 250
			},
			{
				"label": _("Base Imponible"),
				"fieldname": "base_imponible",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Monto Impuesto"),
				"fieldname": "monto_impuesto",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Base Imponible Exportación"),
				"fieldname": "base_imponible_exportacion",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Monto Impuesto Exportación"),
				"fieldname": "monto_impuesto_exportacion",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Base Imponible no Gravada"),
				"fieldname": "base_imponible_no_gravada",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Monto Impuesto No Gravada"),
				"fieldname": "monto_impuesto_no_gravada",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Valor Adquisición No Gravada"),
				"fieldname": "valor_adquisicion_no_gravada",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Monto ISC"),
				"fieldname": "monto_isc",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},			
			{
				"label": _("Otros Conceptos"),
				"fieldname": "otros_conceptos",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Valor Adquisición"),
				"fieldname": "valor_adquisicion",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"fieldname": "moneda",
				"label": _("Moneda"),
				"fieldtype": "Link",
				"options": "Currency",
				"width": 100
			},
			{
				"label": _("Tipo Cambio"),
				"fieldname": "tipo_cambio",
				"fieldtype": "Currency",
				"options": "currency",
				"width": 120
			},
			{
				"label": _("Fecha Inicial Devolución"),
				"fieldtype": "Data",
				"fieldname": "fecha_inicial_devolucion",
				"width": 90
			},
			{
				"label": _("Tipo Devolución"),
				"fieldtype": "Link",
				"fieldname": "tipo_devolucion",
				"options": "Tipos de Comprobante",
				"width": 90
			},	
			{
				"fieldname": "serie_devolucion",
				"label": _("Serie Devolución"),
				"fieldtype": "Data",
				"width": 90
			},
			{
				"fieldname": "dua",
				"label": _("DUA"),
				"fieldtype": "Data",
				"width": 90
			},
			{
				"fieldname": "numero_devolucion",
				"label": _("Número Devolución"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"label": _("Fecha Detracción"),
				"fieldtype": "Data",
				"fieldname": "fecha_detraccion",
				"width": 90
			},
			{
				"fieldname": "constancia_detraccion",
				"label": _("Constancia Detraccion"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "marca_retencion",
				"label": _("Marca Retencion"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "clasificacion_items",
				"label": _("Clasificación Items"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "contrato",
				"label": _("Contrato"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "error_1",
				"label": _("Error 1"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "error_2",
				"label": _("Error 2"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "error_3",
				"label": _("Error 3"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "error_4",
				"label": _("Error 4"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "indicador_pago",
				"label": _("Indicador Pago"),
				"fieldtype": "Data",
				"width": 120
			},
			{
				"fieldname": "anotacion",
				"label": _("Anotación"),
				"fieldtype": "Data",
				"width": 120
			}]
		return columns

	def get_data(self):
		purchase_invoices = self.get_purchase_invoices()
		data = []
		for d in purchase_invoices:
			data.append({
				'periodo': d.periodo,
				'cuo': d.cuo,
				'correlativo_asiento': d.correlativo_asiento,
				'fecha_emision': d.fecha_emision,
				'fecha_cancelacion': d.fecha_cancelacion,
				'codigo_tipo_comprobante': d.tipo_comprobante,
				'serie_comprobante': d.serie_comprobante,
				'codigo_DUA': d.codigo_dua,
				'numero_comprobante': d.numero_comprobante,
				'resumen_diario': d.resumen_diario,
				'tipo_documento': d.tipo_documento,
				'numero_documento': d.numero_documento,
				'nombre_proveedor': d.nombre_proveedor,
				'base_imponible': d.base_imponible,
				'monto_impuesto': d.monto_impuesto,
				'base_imponible_exportacion': d.base_imponible_exportacion,
				'monto_impuesto_exportacion': d.monto_impuesto_exportacion,
				'base_imponible_no_gravada': d.base_imponible_no_gravada,
				'monto_impuesto_no_gravada': d.monto_impuesto_no_gravada,
				'valor_adquisicion_no_gravada': d.valor_adquisicion_no_gravada,
				'monto_isc': d.monto_isc,
				'otros_conceptos': d.otros_conceptos,
				'valor_adquisicion': d.valor_adquisicion,
				'moneda': d.moneda,
				'tipo_cambio': d.tipo_cambio,
				'fecha_inicial_devolucion': d.fecha_inicial_devolucion,
				'tipo_devolucion': d.tipo_devolucion,
				'serie_devolucion': d.serie_devolucion,
				'dua': d.dua,
				'numero_devolucion': d.numero_devolucion,
				'fecha_detraccion': d.fecha_detraccion,
				'constancia_detraccion': d.constancia_detraccion,
				'marca_retencion': d.marca_retencion,
				'clasificacion_items': d.clasificacion_items,
				'contrato': d.contrato,
				'error_1': d.error_1,
				'error_2': d.error_2,
				'error_3': d.error_3,
				'error_4': d.error_4,
				'indicador_pago': d.indicador_pago,
				'anotacion': d.anotacion
				})
		return data

	def run(self):
		columns = self.get_columns()
		data = self.get_data()
		return columns, data

	def get_purchase_invoices(self):
		from_date, to_date = self.get_dates(self.filters.year, self.filters.month)
		from_date_detraction = datetime.datetime.strptime(from_date, '%Y-%m-%d')
		from_date_detraction = self.get_work_days(from_date_detraction, 5)
		to_date_detraction = datetime.datetime.strptime(to_date, '%Y-%m-%d')
		to_date_detraction = self.get_work_days(to_date_detraction, 5)
		purchase_invoices = frappe.db.sql("""(select      
					CONCAT(DATE_FORMAT(IFNULL(posting_date,bill_date),'%Y%m'),'00') as periodo,
					REPLACE(purchase_invoice.name, '-', '') as cuo,
					'M2' as correlativo_asiento,
					DATE_FORMAT(IFNULL(bill_date,posting_date),'%d/%m/%Y') as fecha_emision,
					DATE_FORMAT(IFNULL(bill_expiration_date,posting_date),'%d/%m/%Y') as fecha_cancelacion,
					IF(LENGTH(codigo_comprobante) = 1,CONCAT('0',codigo_comprobante), codigo_comprobante) as tipo_comprobante,
					bill_series as serie_comprobante,
					"" as codigo_dua,
					bill_no as numero_comprobante,
					"" as resumen_diario,
					IF(LENGTH(codigo_tipo_documento)=2,SUBSTRING(codigo_tipo_documento,2),codigo_tipo_documento) as tipo_documento,
					tax_id as numero_documento,
					supplier_name as nombre_proveedor,
					ROUND(IF(base_total_taxes_and_charges=0 OR codigo_comprobante='03', 0, base_net_total - IF(base_inafected_taxes_and_charges=0, 0, base_inafected_taxes_and_charges)), 2) as base_imponible,
					ROUND(IF(codigo_comprobante!='03',base_total_taxes_and_charges,0), 2) as monto_impuesto,
					"" as base_imponible_exportacion,
					"" as monto_impuesto_exportacion,
					"" as base_imponible_no_gravada,
					"" as monto_impuesto_no_gravada,
					ROUND(IF(base_total_taxes_and_charges=0, base_grand_total, IF(base_inafected_taxes_and_charges=0, 0, base_inafected_taxes_and_charges)), 2) as valor_adquisicion_no_gravada,
					"" as monto_isc,
					"" as otros_conceptos,
					ROUND(base_grand_total, 2) as valor_adquisicion,
					IF(currency = 'SOL', 'PEN', currency) as moneda,
					SUBSTRING(conversion_rate,1,POSITION('.' in conversion_rate)+3)  as tipo_cambio,
					IF(is_return,(SELECT DATE_FORMAT(purchase_return.bill_date,'%d/%m/%Y') FROM `tabPurchase Invoice` as purchase_return WHERE purchase_return.name=purchase_invoice.return_against),IF(purchase_invoice.codigo_comprobante='08',(SELECT DATE_FORMAT(purchase_return.bill_date,'%d/%m/%Y') FROM `tabPurchase Invoice` as purchase_return WHERE purchase_return.name=purchase_invoice.debit_note_against),"")) as fecha_inicial_devolucion,
					IF(is_return,(SELECT purchase_return.codigo_comprobante FROM `tabPurchase Invoice`as purchase_return WHERE purchase_return.name=purchase_invoice.return_against),IF(purchase_invoice.codigo_comprobante='08',(SELECT purchase_return.codigo_comprobante FROM `tabPurchase Invoice` as purchase_return WHERE purchase_return.name=purchase_invoice.debit_note_against),"")) as tipo_devolucion,
					IF(is_return,(SELECT purchase_return.bill_series FROM `tabPurchase Invoice`as purchase_return WHERE purchase_return.name=purchase_invoice.return_against),IF(purchase_invoice.codigo_comprobante='08',(SELECT purchase_return.bill_series FROM `tabPurchase Invoice` as purchase_return WHERE purchase_return.name=purchase_invoice.debit_note_against),"")) as serie_devolucion,
					"" as dua,
					IF(is_return,(SELECT purchase_return.bill_no FROM `tabPurchase Invoice` as purchase_return WHERE name=purchase_invoice.return_against),"") as numero_devolucion,
					"" as fecha_detraccion,
					"" as constancia_detraccion,
					"" as marca_retencion,
					"" as clasificacion_items,
					"" as contrato,
					"" as error_1,
					"" as error_2,
					"" as error_3,
					"" as error_4,
					'1' as indicador_pago,
					IF(is_return,(SELECT IF(bill_date>='"""+str(from_date)+"""' AND bill_date<='"""+str(to_date)+"""','1','9') FROM `tabPurchase Invoice` WHERE name=return_against),IF(total_taxes_and_charges=0,'0',IF(bill_date>='"""+str(from_date)+"""' AND bill_date<='"""+str(to_date)+"""','1','6'))) as anotacion
				from
					`tabPurchase Invoice` purchase_invoice
				where posting_date >= '"""+str(from_date)+"""'
				and posting_date <= '"""+str(to_date)+"""'
				and docstatus = 1
				and tdx_c_checkspot = 0
				and is_factoring != 1
				and codigo_comprobante!='02'
				order by posting_date)""", as_dict=True)

		purchase_invoices_detraction = frappe.db.sql("""select
				CONCAT(DATE_FORMAT('"""+str(from_date)+"""','%Y%m'),'00') as periodo,
				REPLACE(purchase_invoice.name, '-', '') as cuo,
				'M2' as correlativo_asiento,
				DATE_FORMAT(IFNULL(bill_date,posting_date),'%d/%m/%Y') as fecha_emision,
				DATE_FORMAT(IFNULL(bill_expiration_date,posting_date),'%d/%m/%Y') as fecha_cancelacion,
				IF(LENGTH(codigo_comprobante) = 1,CONCAT('0',codigo_comprobante), codigo_comprobante) as tipo_comprobante,
				bill_series as serie_comprobante,
				"" as codigo_dua,
				bill_no as numero_comprobante,
				"" as resumen_diario,
				IF(LENGTH(codigo_tipo_documento)=2,SUBSTRING(codigo_tipo_documento,2),codigo_tipo_documento) as tipo_documento,
				tax_id as numero_documento,
				supplier_name as nombre_proveedor,
				ROUND(IF(base_total_taxes_and_charges=0 OR codigo_comprobante='03', 0, base_net_total - IF(base_inafected_taxes_and_charges=0, 0, base_inafected_taxes_and_charges)), 2) as base_imponible,
				ROUND(IF(codigo_comprobante!='03',base_total_taxes_and_charges,0), 2) as monto_impuesto,
				"" as base_imponible_exportacion,
				"" as monto_impuesto_exportacion,
				"" as base_imponible_no_gravada,
				"" as monto_impuesto_no_gravada,
				ROUND(IF(base_total_taxes_and_charges=0, base_grand_total, IF(base_inafected_taxes_and_charges=0, 0, base_inafected_taxes_and_charges)), 2) as valor_adquisicion_no_gravada,
				"" as monto_isc,
				"" as otros_conceptos,
				ROUND(base_grand_total, 2) as valor_adquisicion,
				IF(currency = 'SOL', 'PEN', currency) as moneda,
				SUBSTRING(conversion_rate,1,POSITION('.' in conversion_rate)+3)  as tipo_cambio,
				IF(is_return,(SELECT purchase_return.bill_date FROM `tabPurchase Invoice` as purchase_return WHERE purchase_return.name=purchase_invoice.return_against),IF(purchase_invoice.codigo_comprobante='08',(SELECT purchase_return.bill_date FROM `tabPurchase Invoice` as purchase_return WHERE purchase_return.name=purchase_invoice.debit_note_against),"")) as fecha_inicial_devolucion,
				IF(is_return,(SELECT purchase_return.codigo_comprobante FROM `tabPurchase Invoice`as purchase_return WHERE purchase_return.name=purchase_invoice.return_against),IF(purchase_invoice.codigo_comprobante='08',(SELECT purchase_return.codigo_comprobante FROM `tabPurchase Invoice` as purchase_return WHERE purchase_return.name=purchase_invoice.debit_note_against),"")) as tipo_devolucion,
				IF(is_return,(SELECT purchase_return.bill_series FROM `tabPurchase Invoice`as purchase_return WHERE purchase_return.name=purchase_invoice.return_against),IF(purchase_invoice.codigo_comprobante='08',(SELECT purchase_return.bill_series FROM `tabPurchase Invoice` as purchase_return WHERE purchase_return.name=purchase_invoice.debit_note_against),"")) as serie_devolucion,
				"" as dua,
				IF(is_return,(SELECT purchase_return.bill_no FROM `tabPurchase Invoice` as purchase_return WHERE name=purchase_invoice.return_against),"") as numero_devolucion,
				DATE_FORMAT(det.`tdx_c_figv_fechaconstancia`,'%d/%m/%Y') as fecha_detraccion,
				det.`tdx_c_figv_constancia` as constancia_detraccion,
				"" as marca_retencion,
				"" as clasificacion_items,
				"" as contrato,
				"" as error_1,
				"" as error_2,
				"" as error_3,
				"" as error_4,
				'1' as indicador_pago,
				IF(is_return,(SELECT IF(bill_date>='"""+str(from_date_detraction.strftime('%Y-%m-%d'))+"""' AND bill_date<='"""+str(to_date_detraction.strftime('%Y-%m-%d'))+"""','1','9') FROM `tabPurchase Invoice` WHERE name=return_against),IF(total_taxes_and_charges=0,'0',IF(bill_date>='"""+str(from_date_detraction.strftime('%Y-%m-%d'))+"""' AND bill_date<='"""+str(to_date_detraction.strftime('%Y-%m-%d'))+"""','1','6'))) as anotacion
			from
				`tabPurchase Invoice` purchase_invoice,
				`tabFiscalizacion del IGV Compra` det
			where det.parent = purchase_invoice.name
			and det.`tdx_c_figv_fechaconstancia` >= '"""+str(from_date_detraction.strftime('%Y-%m-%d'))+"""' 
			and det.`tdx_c_figv_fechaconstancia` <= '"""+str(to_date_detraction.strftime('%Y-%m-%d'))+"""' 
			and purchase_invoice.docstatus = 1
			and codigo_comprobante!='02'
			and is_factoring != 1
			order by det.`tdx_c_figv_fechaconstancia`
		""", as_dict=True)

		purchase_invoices += purchase_invoices_detraction

		return purchase_invoices

def execute(filters=None):
	columns, data = PLECompras(filters).run()
	
	return columns, data
