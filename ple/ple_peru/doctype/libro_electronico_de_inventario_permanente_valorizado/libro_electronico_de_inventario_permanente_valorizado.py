# -*- coding: utf-8 -*-
# Copyright (c) 2018, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from ple.ple_peru.utils import Utils, to_file

class LibroElectronicodeInventarioPermanenteValorizado(Utils):
	def get_inventory(self, year, periodo):
		inventory_list = []
		from_date, to_date = self.get_dates(year, periodo)

		inventories = frappe.db.sql("""select
					CONCAT(DATE_FORMAT(due_date,'%Y%m'),'00') as periodo,
					REPLACE(inventory.voucher_no, '-', '') as cuo,
					CONCAT('M', IF(voucher_type = 'Stock Entry', 
					(SELECT 
						COUNT(name)
					FROM
						`tabStock Ledger Entry` as stock_1
					WHERE stock_1.voucher_no = stock.voucher_no
					AND SUBSTRING(stock_1.account, 1, 2) <= SUBSTRING(stock.account, 1, 2)),
					(SELECT 
						COUNT(name)
					FROM
						`tabStock Ledger Entry` as stock_1
					WHERE stock_1.voucher_no = stock.voucher_no
					AND SUBSTRING(stock_1.account, 1, 2) >= SUBSTRING(stock.account, 1, 2)))) as correlativo_asiento,
					(SELECT codigo_almacen_sunat FROM `tabWarehouse` as wh WHERE wh.company=stock.company AND wh.name=stock.warehouse) as almacen,
					comp.codigo_catalogo_existencias as codigo_catalogo,
					pro.codigo_tipo_existencia,
					IF(pro.codigo_sunat, pro.codigo_sunat, pro.name) as codigo_producto,
					IF(comp.codigo_catalogo_existencias='9',"",pro.codigo_sunat) as codigo_sunat,
					DATE_FORMAT(stock.posting_date,'%d/%m/%Y') as fecha_emision,
					"" as resumen_diario,
					IF(base_net_total>700,codigo_tipo_documento,IF(ISNULL(tax_id),"",IFNULL(codigo_tipo_documento,""))) as tipo_documento,
					IF(codigo_tipo_documento=7,IF(SUBSTRING(REPLACE(tax_id,"-",""),-12)="",tax_id, SUBSTRING(REPLACE(tax_id,"-",""),-12)),IF(base_net_total>700,tax_id,IF(ISNULL(tax_id),"",tax_id))) as numero_documento,
					IF(base_net_total>700,customer_name,IF(ISNULL(tax_id),"",IF(customer_name='Clientes Varios',customer_boleta_name,customer_name))) as nombre_cliente,
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
					IF(currency = 'SOL', 'PEN', currency) as moneda,
					SUBSTRING(conversion_rate,1,POSITION('.' in conversion_rate)+3) as tipo_cambio,
					IF(is_return,(SELECT due_date FROM `tabSales Invoice` WHERE name=return_against),"") as fecha_inicial_devolucion,
					IF(is_return,(SELECT codigo_comprobante FROM `tabSales Invoice` WHERE name=return_against),"") as tipo_devolucion,
					IF(is_return,SUBSTRING((SELECT name FROM `tabSales Invoice` WHERE name=return_against),4,3),"") as serie_devolucion,
					IF(is_return,SUBSTRING((SELECT name FROM `tabSales Invoice` WHERE name=return_against),8),"")  as dua,
					"" as contrato,
					"" as error_1,
					'1' as indicador_pago,
					IF(inventory.docstatus='2','2',IF(CONCAT(DATE_FORMAT(posting_date,'%Y-%m'),'-01')>=due_date,'7','1')) as anotacion
				from
					`tabStock Ledger Entry` as stock,
					`tabCompany` as comp,
					`tabItem` as pro
				where comp.name = stock.company
				and pro.name = stock.item_code
				and due_date > '""" + str(from_date) + """' 
				and due_date < '""" + str(to_date) + """' 
				order by due_date""", as_dict=True)

		for d in inventories:
			inventory_list.append({
				'periodo': d.periodo,
				'cuo': d.cuo,
				'correlativo_asiento': d.almacen,
				'fecha_emision': d.codigo_catalogo,
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
		return inventory_list

	def export_libro_inventarios(self, year, periodo, ruc):
		tipo = "inventario"
		data = self.get_inventory(year, periodo)
		codigo_periodo = self.ple_name(year, periodo)
		nombre = "LE" + str(ruc) + codigo_periodo + '00140100' + '00' + '1' + ('1' if data else '0') + '1' + '1'
		nombre = nombre + ".txt"
		return to_file(data, tipo, nombre)
