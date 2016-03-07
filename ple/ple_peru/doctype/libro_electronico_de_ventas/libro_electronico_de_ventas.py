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

class LibroElectronicodeVentas(Document):
	pass


@frappe.whitelist()
def get_sales_invoices(year, periodo):
	sales_invoice_list = []
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

	sales_invoices = frappe.db.sql("""select
			CONCAT(DATE_FORMAT(due_date,'%Y%m'),'00') as periodo,
			SUBSTRING(journal_entry.parent,4) as cuo,
			CONCAT('M',journal_entry.idx) as correlativo_asiento,
			DATE_FORMAT(posting_date,'%d/%m/%Y') as fecha_emision,
			DATE_FORMAT(due_date,'%d/%m/%Y') as fecha_cancelacion,
			codigo_comprobante as tipo_comprobante,
			SUBSTRING(sales_invoice.name,4,3) as serie_comprobante,
			SUBSTRING(sales_invoice.name,8) as numero_comprobante,
			"" as resumen_diario,
			IF(codigo_tipo_documento=NULL,"",codigo_tipo_documento) as tipo_documento,
			IF(tax_id=NULL,"",tax_id) as numero_documento,
			IF(customer_name='Clientes Varios',customer_boleta_name,customer_name) as nombre_cliente,
			"" as valor_exportacion,
			base_net_total as base_imponible,
			"" as descuento,
			total_taxes_and_charges as monto_impuesto,
			"" as descuento_igv,
			"" as total_exonerado,
			"" as total_inafecto,
			"" as monto_isc,
			"" as base_arroz,
			"" as impuesto_arroz,	
			"" as otros_conceptos,		
			grand_total as valor_adquisicion,
			currency as moneda,
			conversion_rate as tipo_cambio,
			IF(is_return,(SELECT due_date FROM `tabSales Invoice` WHERE name=return_against),"") as fecha_inicial_devolucion,
			IF(is_return,(SELECT codigo_comprobante FROM `tabSales Invoice` WHERE name=return_against),"") as tipo_devolucion,
			IF(is_return,SUBSTRING((SELECT name FROM `tabSales Invoice` WHERE name=return_against),4,3),"") as serie_devolucion,
			IF(is_return,SUBSTRING((SELECT name FROM `tabSales Invoice` WHERE name=return_against),8),"")  as dua,
			"" as contrato,
			"" as error_1,
			'1' as indicador_pago,
			IF(posting_date<due_date,'8','1') as anotacion
		from
			`tabSales Invoice` sales_invoice
		left join
			`tabJournal Entry Account` journal_entry
		on journal_entry.reference_name = sales_invoice.name
		where due_date > '"""+str(from_date)+"""' 
		and due_date < '"""+str(to_date)+"""' 
		order by due_date""", as_dict=True)

	for d in sales_invoices:
		sales_invoice_list.append({
			'periodo': d.periodo,
			'cuo': d.cuo,
			'correlativo_asiento': d.correlativo_asiento,
			'fecha_emision': d.fecha_emision,
			'fecha_cancelacion': d.fecha_cancelacion,
			'codigo_tipo_comprobante': d.tipo_comprobante,
			'serie_comprobante': d.serie_comprobante,
			'numero_comprobante': d.numero_comprobante,
			'resumen_diario': d.resumen_diario,
			'tipo_documento': d.tipo_documento,
			'numero_documento': d.numero_documento,
			'nombre_cliente': d.nombre_cliente,
			'valor_exportacion': d.valor_exportacion,
			'base_imponible': d.base_imponible,
			'descuento': d.descuento,
			'monto_impuesto': d.monto_impuesto,
			'descuento_igv': d.descuento_igv,
			'total_exonerado': d.total_exonerado,
			'total_inafecto': d.total_inafecto,
			'monto_isc': d.monto_isc,
			'base_arroz': d.base_arroz,
			'impuesto_arroz': d.impuesto_arroz,
			'otros_conceptos': d.otros_conceptos,
			'valor_adquisicion': d.valor_adquisicion,
			'moneda': d.moneda,
			'tipo_cambio': d.tipo_cambio,
			'fecha_inicial_devolucion': d.fecha_inicial_devolucion,
			'tipo_devolucion': d.tipo_devolucion,
			'serie_devolucion': d.serie_devolucion,
			'dua': d.dua,
			'contrato': d.contrato,
			'error_1': d.error_1,
			'indicador_pago': d.indicador_pago,
			'anotacion': d.anotacion
			})
	return sales_invoice_list


@frappe.whitelist()
def export_libro_de_ventas(year, periodo, ruc):
	tipo = "ventas"
	codigo_periodo = ""
	data = get_sales_invoices(year, periodo)
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
		codigo_periodo = year + "610"
	elif periodo=='Noviembre':
		codigo_periodo = year + "11"
	elif periodo=='Diciembre':
		codigo_periodo = year + "12"
	nombre = "LE"+str(ruc)+codigo_periodo+'140100'+'00'+'1'+'1'+'1'+'1'
	send_txt_to_client(data,nombre, tipo)



