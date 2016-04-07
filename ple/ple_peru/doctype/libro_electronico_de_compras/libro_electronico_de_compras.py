# -*- coding: utf-8 -*-
# Copyright (c) 2015, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months
from frappe import throw, _
from frappe.utils import formatdate
import frappe.desk.reportview

from ple.ple_peru.utils import send_txt_to_client

class LibroElectronicodeCompras(Document):
	pass


@frappe.whitelist()
def get_purchase_invoices(year, periodo):
	purchase_invoice_list = []
	from_date = ""
	to_date = ""
	if periodo=='Enero':
		from_date=year+'-01-01'
		to_date=year+'-01-31'
	elif periodo=='Febrero':
		from_date=year+'-02-01'
		to_date=year+'-02-29'
	elif periodo=='Marzo':
		from_date=year+'-03-01'
		to_date=year+'-03-31'
	elif periodo=='Abril':
		from_date=year+'-04-01'
		to_date=year+'-04-30'
	elif periodo=='Mayo':
		from_date=year+'-05-01'
		to_date=year+'-05-29'
	elif periodo=='Junio':
		from_date=year+'-06-01'
		to_date=year+'-06-30'
	elif periodo=='Julio':
		from_date=year+'-07-01'
		to_date=year+'-07-31'
	elif periodo=='Agosto':
		from_date=year+'-08-01'
		to_date=year+'-08-31'
	elif periodo=='Setiembre':
		from_date=year+'-09-01'
		to_date=year+'-09-30'
	elif periodo=='Octubre':
		from_date=year+'-10-10'
		to_date=year+'-10-31'
	elif periodo=='Noviembre':
		from_date=year+'-11-01'
		to_date=year+'-11-30'
	elif periodo=='Diciembre':
		from_date=year+'-12-01'
		to_date=year+'-12-31'

	purchase_invoices = frappe.db.sql("""select      
			CONCAT(DATE_FORMAT(posting_date,'%Y%m'),'00') as periodo,
			SUBSTRING(journal_entry.parent,4) as cuo,
			CONCAT('M',journal_entry.idx) as correlativo_asiento,
			DATE_FORMAT(IFNULL(bill_date,posting_date),'%d/%m/%Y') as fecha_emision,
			DATE_FORMAT(IFNULL(bill_expiration_date,posting_date),'%d/%m/%Y') as fecha_cancelacion,
			codigo_tipo_comprobante as tipo_comprobante,
			CONCAT('0',IFNULL(bill_series,'0000')) as serie_comprobante,
			"" as codigo_dua,
			bill_no as numero_comprobante,
			"" as resumen_diario,
			codigo_tipo_documento as tipo_documento,
			tax_id as numero_documento,
			supplier_name as nombre_proveedor,
			base_net_total as base_imponible,
			taxes_and_charges_added as monto_impuesto,
			"" as base_imponible_exportacion,
			"" as monto_impuesto_exportacion,
			"" as base_imponible_no_gravada,
			"" as monto_impuesto_no_gravada,
			"" as valor_adquisicion_no_gravada,
			"" as monto_isc,
			"" as otros_conceptos,			
			grand_total as valor_adquisicion,
			currency as moneda,
			'1.000'  as tipo_cambio,
			IF(is_return,(SELECT bill_date FROM `tabPurchase Invoice` WHERE name=return_against),"") as fecha_inicial_devolucion,
			IF(is_return,(SELECT codigo_tipo_comprobante FROM `tabPurchase Invoice` WHERE name=return_against),"") as tipo_devolucion,
			IF(is_return,(SELECT bill_series FROM `tabPurchase Invoice` WHERE name=return_against),"") as serie_devolucion,
			"" as dua,
			IF(is_return,(SELECT bill_no FROM `tabPurchase Invoice` WHERE name=return_against),"") as numero_devolucion,
			IF(is_return,posting_date,"") as fecha_devolucion,
			"" as detraccion,
			"" as marca_detraccion,
			"" as clasificacion_items,
			"" as contrato,
			"" as error_1,
			"" as error_2,
			"" as error_3,
			"" as error_4,
			'1' as indicador_pago,
			IF(bill_expiration_date<bill_date,'8','1') as anotacion
		from
			`tabPurchase Invoice` purchase_invoice
		left join
            `tabJournal Entry Account` journal_entry
		on journal_entry.reference_name = purchase_invoice.name
		where bill_expiration_date > '"""+str(from_date)+"""' 
		and bill_expiration_date < '"""+str(to_date)+"""' 
		order by bill_expiration_date""", as_dict=True)

	for d in purchase_invoices:
		purchase_invoice_list.append({
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
			'fecha_devolucion': d.fecha_devolucion,
			'detraccion': d.detraccion,
			'marca_detraccion': d.marca_detraccion,
			'clasificacion_items': d.clasificacion_items,
			'contrato': d.contrato,
			'error_1': d.error_1,
			'error_2': d.error_2,
			'error_3': d.error_3,
			'error_4': d.error_4,
			'indicador_pago': d.indicador_pago,
			'anotacion': d.anotacion
			})
	return purchase_invoice_list


@frappe.whitelist()
def export_libro_de_compras(year, periodo, ruc):
	tipo = "compras"
	codigo_periodo = ""
	data = get_purchase_invoices(year, periodo)
	if periodo=='Enero':
		codigo_periodo = year + "01"
	elif periodo=='Febrero':
		codigo_periodo = year + "02"
	elif periodo=='Marzo':
		codigo_periodo = year + "03"
	elif periodo=='Abril':
		codigo_periodo = year + "04"
	elif periodo=='Mayo':
		codigo_periodo = year + "05"
	elif periodo=='Junio':
		codigo_periodo = year + "06"
	elif periodo=='Julio':
		codigo_periodo = year + "07"
	elif periodo=='Agosto':
		codigo_periodo = year + "08"
	elif periodo=='Setiembre':
		codigo_periodo = year + "09"
	elif periodo=='Octubre':
		codigo_periodo = year + "10"
	elif periodo=='Noviembre':
		codigo_periodo = year + "11"
	elif periodo=='Diciembre':
		codigo_periodo = year + "12"
	nombre = "LE"+str(ruc)+codigo_periodo+'00080100'+'00'+'1'+'1'+'1'+'1'
	send_txt_to_client(data,nombre, tipo)


@frappe.whitelist()
def export_libro_de_compras_vacio(year, periodo, ruc):
	tipo = "compras"
	codigo_periodo = ""
	data = ""
	if periodo=='Enero':
		codigo_periodo = year + "01"
	elif periodo=='Febrero':
		codigo_periodo = year + "02"
	elif periodo=='Marzo':
		codigo_periodo = year + "03"
	elif periodo=='Abril':
		codigo_periodo = year + "04"
	elif periodo=='Mayo':
		codigo_periodo = year + "05"
	elif periodo=='Junio':
		codigo_periodo = year + "06"
	elif periodo=='Julio':
		codigo_periodo = year + "07"
	elif periodo=='Agosto':
		codigo_periodo = year + "08"
	elif periodo=='Setiembre':
		codigo_periodo = year + "09"
	elif periodo=='Octubre':
		codigo_periodo = year + "10"
	elif periodo=='Noviembre':
		codigo_periodo = year + "11"
	elif periodo=='Diciembre':
		codigo_periodo = year + "12"
	nombre = "LE"+str(ruc)+codigo_periodo+'00080200'+'00'+'1'+'0'+'1'+'1'
	send_txt_to_client(data,nombre, tipo)


