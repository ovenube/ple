# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
import json
import csv, cStringIO
from frappe.utils import encode, cstr, cint, flt, comma_or
from frappe.website.context import get_context
import frappe.api


@frappe.whitelist()
def send_txt_to_client(data, nombre, tipo, primer=None):
	file = to_txt(data, tipo, nombre, primer)
	data = read_txt(file)
	frappe.response['result'] = cstr(data)
	frappe.response['type'] = 'txt'
	frappe.response['doctype'] = nombre


@frappe.whitelist()
def send_csv_to_client(data, nombre, tipo):
	file = to_csv(data, tipo, nombre)
	data = read_txt(file)
	frappe.response['result'] = cstr(data)
	frappe.response['type'] = 'csv'
	frappe.response['doctype'] = nombre


def to_txt(data, tipo, nombre, primer=None):
	archivo = nombre+".txt"
	exported_file = open(archivo,"w")	
	if tipo=="compras":
		for row in data:
			exported_file.write(
				row['periodo']+'|'+
				row['cuo']+'|'+
				row['correlativo_asiento']+'|'+
				str(row['fecha_emision'])+'|'+
				str(row['fecha_cancelacion'])+'|'+
				row['codigo_tipo_comprobante']+'|'+
				row['serie_comprobante']+'|'+
				row['codigo_DUA']+'|'+
				row['numero_comprobante']+'|'+
				row['resumen_diario']+'|'+
				row['tipo_documento']+'|'+
				row['numero_documento']+'|'+
				row['nombre_proveedor']+'|'+
				str(row['base_imponible'])+'|'+
				str(row['monto_impuesto'])+'|'+
				row['base_imponible_exportacion']+'|'+
				row['monto_imppuesto_exportacion']+'|'+
				row['base_imponible_no_gravada']+'|'+
				row['monto_imppuesto_no_gravada']+'|'+
				row['valor_adquisicion_no_gravada']+'|'+
				row['monto_isc']+'|'+
				row['otros_conceptos']+'|'+
				str(row['valor_adquisicion'])+'|'+
				row['moneda']+'|'+
				str(row['tipo_cambio'])+'|'+
				row['fecha_inicial_devolucion']+'|'+
				row['tipo_devolucion']+'|'+
				row['serie_devolucion']+'|'+
				row['dua']+'|'+
				row['numero_devolucion']+'|'+
				row['fecha_devolucion']+'|'+
				row['detraccion']+'|'+
				row['marca_detraccion']+'|'+
				row['clasificacion_items']+'|'+
				row['contrato']+'|'+
				row['error_1']+'|'+
				row['error_2']+'|'+
				row['error_3']+'|'+
				row['error_4']+'|'+
				str(row['indicador_pago'])+'|'+
				str(row['anotacion']+'\n'))
	elif tipo=="ventas":
		for row in data:
			exported_file.write(
				row['periodo']+"|"+
				row['cuo']+"|"+
				row['correlativo_asiento']+"|"+
				str(row['fecha_emision'])+"|"+
				str(row['fecha_cancelacion'])+"|"+
				row['codigo_tipo_comprobante']+"|"+
				row['serie_comprobante']+"|"+
				row['numero_comprobante']+"|"+
				row['resumen_diario']+"|"+
				row['tipo_documento']+"|"+
				row['numero_documento']+"|"+
				unicode(row['nombre_cliente'])+"|"+
				row['valor_exportacion']+"|"+
				str(row['base_imponible'])+"|"+
				row['descuento']+"|"+
				str(row['monto_impuesto'])+"|"+
				row['descuento_igv']+"|"+
				row['total_exonerado']+"|"+
				row['total_inafecto']+"|"+
				row['monto_isc']+"|"+
				row['base_arroz']+"|"+
				row['impuesto_arroz']+"|"+
				row['otros_conceptos']+"|"+
				str(row['valor_adquisicion'])+"|"+
				row['moneda']+"|"+
				str(row['tipo_cambio'])+"|"+
				str(row['fecha_inicial_devolucion'])+"|"+
				str(row['tipo_devolucion'])+"|"+
				str(row['serie_devolucion'])+"|"+
				str(row['dua'])+"|"+
				row['contrato']+"|"+
				row['error_1']+"|"+
				str(row['indicador_pago'])+"|"+
				str(row['anotacion']+"\n"))
	elif tipo=="diario":
		if primer=="1":
			for row in data:
				exported_file.write(
				row['periodo']+"|"+
				row['codigo_asiento']+"|"+
				row['descripcion_asiento']+"|"+
				row['codigo_plan']+"|"+
				row['descripcion_plan']+"|"+
				row['codigo_cuenta']+"|"+
				row['descripcion_cuenta']+"|"+
				row['indicador_cuenta']+"\n")
		else:
			for row in data:
				exported_file.write(
				row['periodo']+"|"+
				row['cuo']+"|"+
				row['correlativo_asiento']+"|"+
				row['codigo_asiento']+"|"+
				row['cuo_ue']+"|"+
				row['centro_costo']+"|"+
				row['tipo_moneda']+"|"+
				row['tipo_documento']+"|"+
				row['codigo_comprobante']+"|"+
				row['serie_comprobante']+"|"+
				row['numero_comprobante']+"|"+
				str(row['fecha_contable'])+"|"+
				str(row['fecha_emision'])+"|"+
				str(row['fecha_vencimiento'])+"|"+
				row['glosa']+"|"+
				str(row['debe'])+"|"+
				str(row['haber'])+"|"+
				row['estructurado']+"|"+
				str(row['estado']+"\n"))

	return archivo


def to_csv(data, tipo, nombre, primer=None):
	archivo = nombre+".txt"
	exported_file = open(archivo,"w")	
	if tipo=="Compras":
		exported_file.write(
			'Libro Electronico de Compras'+'\n'
			'periodo'+','+
			'cuo'+','+
			'correlativo_asiento'+','+
			'fecha_emision'+','+
			'fecha_cancelacion'+','+
			'codigo_tipo_comprobante'+','+
			'serie_comprobante'+','+
			'codigo_DUA'+','+
			'numero_comprobante'+','+
			'resumen_diario'+','+
			'tipo_documento'+','+
			'numero_documento'+','+
			'nombre_proveedor'+','+
			'base_imponible'+','+
			'monto_impuesto'+','+
			'base_imponible_exportacion'+','+
			'monto_imppuesto_exportacion'+','+
			'base_imponible_no_gravada'+','+
			'monto_imppuesto_no_gravada'+','+
			'valor_adquisicion_no_gravada'+','+
			'monto_isc'+','+
			'otros_conceptos'+','+
			'valor_adquisicion'+','+
			'moneda'+','+
			'tipo_cambio'+','+
			'fecha_inicial_devolucion'+','+
			'tipo_devolucion'+','+
			'serie_devolucion'+','+
			'dua'+','+
			'numero_devolucion'+','+
			'fecha_devolucion'+','+
			'detraccion'+','+
			'marca_detraccion'+','+
			'clasificacion_items'+','+
			'contrato'+','+
			'error_1'+','+
			'error_2'+','+
			'error_3'+','+
			'error_4'+','+
			'indicador_pago'+','+
			'anotacion'+'\n')
		for row in data:
			exported_file.write(
				row['periodo']+','+
				row['cuo']+','+
				row['correlativo_asiento']+','+
				str(row['fecha_emision'])+','+
				str(row['fecha_cancelacion'])+','+
				row['codigo_tipo_comprobante']+','+
				row['serie_comprobante']+','+
				row['codigo_DUA']+','+
				row['numero_comprobante']+','+
				row['resumen_diario']+','+
				row['tipo_documento']+','+
				row['numero_documento']+','+
				row['nombre_proveedor']+','+
				str(row['base_imponible'])+','+
				str(row['monto_impuesto'])+','+
				row['base_imponible_exportacion']+','+
				row['monto_imppuesto_exportacion']+','+
				row['base_imponible_no_gravada']+','+
				row['monto_imppuesto_no_gravada']+','+
				row['valor_adquisicion_no_gravada']+','+
				row['monto_isc']+','+
				row['otros_conceptos']+','+
				str(row['valor_adquisicion'])+','+
				row['moneda']+','+
				str(row['tipo_cambio'])+','+
				row['fecha_inicial_devolucion']+','+
				row['tipo_devolucion']+','+
				row['serie_devolucion']+','+
				row['dua']+','+
				row['numero_devolucion']+','+
				row['fecha_devolucion']+','+
				row['detraccion']+','+
				row['marca_detraccion']+','+
				row['clasificacion_items']+','+
				row['contrato']+','+
				row['error_1']+','+
				row['error_2']+','+
				row['error_3']+','+
				row['error_4']+','+
				str(row['indicador_pago'])+','+
				str(row['anotacion']+'\n'))
	elif tipo=="Ventas":
		exported_file.write(
			'Libro Electronico de Ventas'+'\n'
			'periodo'+","+
			'cuo'+","+
			'correlativo_asiento'+","+
			'fecha_emision'+","+
			'fecha_cancelacion'+","+
			'codigo_tipo_comprobante'+","+
			'serie_comprobante'+","+
			'numero_comprobante'+","+
			'resumen_diario'+","+
			'tipo_documento'+","+
			'numero_documento'+","+
			'nombre_cliente'+","+
			'valor_exportacion'+","+
			'base_imponible'+","+
			'descuento'+","+
			'monto_impuesto'+","+
			'descuento_igv'+","+
			'total_exonerado'+","+
			'total_inafecto'+","+
			'monto_isc'+","+
			'base_arroz'+","+
			'impuesto_arroz'+","+
			'otros_conceptos'+","+
			'valor_adquisicion'+","+
			'moneda'+","+
			'tipo_cambio'+","+
			'fecha_inicial_devolucion'+","+
			'tipo_devolucion'+","+
			'serie_devolucion'+","+
			'dua'+","+
			'contrato'+","+
			'error_1'+","+
			'indicador_pago'+","+
			'anotacion'+"\n")
		for row in data:
			exported_file.write(
				row['periodo']+","+
				row['cuo']+","+
				row['correlativo_asiento']+","+
				str(row['fecha_emision'])+","+
				str(row['fecha_cancelacion'])+","+
				row['codigo_tipo_comprobante']+","+
				row['serie_comprobante']+","+
				row['numero_comprobante']+","+
				row['resumen_diario']+","+
				row['tipo_documento']+","+
				row['numero_documento']+","+
				row['nombre_cliente']+","+
				row['valor_exportacion']+","+
				str(row['base_imponible'])+","+
				row['descuento']+","+
				str(row['monto_impuesto'])+","+
				row['descuento_igv']+","+
				row['total_exonerado']+","+
				row['total_inafecto']+","+
				row['monto_isc']+","+
				row['base_arroz']+","+
				row['impuesto_arroz']+","+
				row['otros_conceptos']+","+
				str(row['valor_adquisicion'])+","+
				row['moneda']+","+
				str(row['tipo_cambio'])+","+
				row['fecha_inicial_devolucion']+","+
				row['tipo_devolucion']+","+
				row['serie_devolucion']+","+
				row['dua']+","+
				row['contrato']+","+
				row['error_1']+","+
				str(row['indicador_pago'])+","+
				str(row['anotacion']+"\n"))
	elif tipo=="Diario":
		if primer=="1":
			exported_file.write(
				'Libro Electronico Diario Primero'+'\n'
				'periodo'+","+
				'codigo_asiento'+","+
				'descripcion_asiento'+","+
				'codigo_plan'+","+
				'descripcion_plan'+","+
				'codigo_cuenta'+","+
				'descripcion_cuenta'+","+
				'indicador_cuenta'+"\n")
			for row in data:
				exported_file.write(
					row['periodo']+","+
					row['codigo_asiento']+","+
					row['descripcion_asiento']+","+
					row['codigo_plan']+","+
					row['descripcion_plan']+","+
					row['codigo_cuenta']+","+
					row['descripcion_cuenta']+","+
					row['indicador_cuenta']+"\n")
		else:
			exported_file.write(
				'Libro Electronico Diario'+'\n'
				'periodo'+","+
				'cuo'+","+
				'correlativo_asiento'+","+
				'codigo_asiento'+","+
				'cuo_ue'+","+
				'centro_costo'+","+
				'tipo_moneda'+","+
				'tipo_documento'+","+
				'codigo_comprobante'+","+
				'serie_comprobante'+","+
				'numero_comprobante'+","+
				'fecha_contable'+","+
				'fecha_emision'+","+
				'fecha_vencimiento'+","+
				'glosa'+","+
				'debe'+","+
				'haber'+","+
				'estructurado'+","+
				'estado'+"\n")
			for row in data:
				exported_file.write(
					row['periodo']+",'"+
					row['cuo']+"',"+
					row['correlativo_asiento']+","+
					row['codigo_asiento']+","+
					row['cuo_ue']+","+
					row['centro_costo']+","+
					row['tipo_moneda']+","+
					row['tipo_documento']+","+
					row['codigo_comprobante']+","+
					row['serie_comprobante']+","+
					row['numero_comprobante']+","+
					str(row['fecha_contable'])+","+
					str(row['fecha_emision'])+","+
					row['fecha_vencimiento']+","+
					row['glosa']+","+
					str(row['debe'])+","+
					str(row['haber'])+","+
					row['estructurado']+","+
					str(row['estado']+"\n"))

	return archivo


def read_txt(file):
	data = ""
	exported_file = open(file, 'r')
	for line in exported_file:
		data = data + line
	return data
