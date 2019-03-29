# -*- coding: utf-8 -*-
# Copyright (c) 2018, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from ple.ple_peru.utils import Utils, to_file
from ple.ple_peru.doctype.tipos_de_operaciones.tipos_de_operaciones import get_operacion

class LibroElectronicodeInventarioPermanenteValorizado(Utils):
	def get_inventory(self, year, periodo):
		inventory_list = []
		from_date, to_date = self.get_dates(year, periodo)

		inventories = frappe.db.sql("""select
					CONCAT(DATE_FORMAT(posting_date,'%Y%m'),'00') as periodo,
					REPLACE(stock.voucher_no, '-', '') as cuo,
					CONCAT('M', IF(voucher_type='Stock Entry', 
					(SELECT 
						COUNT(name)
					FROM
						`tabStock Ledger Entry` as stock_1
					WHERE stock_1.voucher_no = stock.voucher_no),
					(SELECT 
						COUNT(name)
					FROM
						`tabStock Ledger Entry` as stock_1
					WHERE stock_1.voucher_no = stock.voucher_no))) as correlativo_asiento,
					(SELECT codigo_almacen_sunat FROM `tabWarehouse` as wh WHERE wh.company=stock.company AND wh.name=stock.warehouse) as almacen,
					comp.codigo_catalogo_existencias as codigo_catalogo,
					pro.codigo_tipo_existencia,
					IF(pro.codigo_sunat, pro.codigo_sunat, pro.name) as codigo_producto,
					IF(comp.codigo_catalogo_existencias='9',"",pro.codigo_sunat) as codigo_sunat,
					DATE_FORMAT(stock.posting_date,'%d/%m/%Y') as fecha_emision,
					IF(stock.voucher_type='Stock Entry','00',
						(IF(stock.voucher_type='Purchase Receipt',(SELECT codigo_tipo_comprobante FROM `tabPurchase Receipt` as pr WHERE pr.name=stock.voucher_no),
						IF(stock.voucher_type='Delivery Note',(SELECT codigo_tipo_comprobante FROM `tabDelivery Note` as dn WHERE dn.name=stock.voucher_no),"")))) as codigo_comprobante,
					IF(stock.voucher_type='Stock Entry','0',
						IF(stock.voucher_type='Delivery Note',SUBSTRING_INDEX(stock.voucher_no,'-',1),
						IF(stock.voucher_type='Purchase Receipt',(SELECT serie_delivery_note FROM `tabPurchase Receipt` as pr WHERE pr.name=stock.voucher_no),'0'))) as serie_comprobante,
					IF(stock.voucher_type='Stock Entry','0',
						IF(stock.voucher_type='Delivery Note',SUBSTRING_INDEX(stock.voucher_no,'-',-1),
						IF(stock.voucher_type='Purchase Receipt',(SELECT supplier_delivery_note FROM `tabPurchase Receipt` as pr WHERE pr.name=stock.voucher_no),'0'))) as correlativo_comprobante,
					IF(stock.voucher_type='Stock Entry',
						IF((SELECT title FROM `tabStock Entry` as se WHERE se.name=stock.voucher_no)='Material Issue',(SELECT codigo_tipo_operacion FROM `tabStock Entry` as se WHERE se.name=stock.voucher_no),
							IF((SELECT title FROM `tabStock Entry` as se WHERE se.name=stock.voucher_no)='Material Receipt','16',
								IF((SELECT title FROM `tabStock Entry` as se WHERE se.name=stock.voucher_no)='Material Transfer',IF(stock.actual_qty>0,'21','11'),
									IF((SELECT title FROM `tabStock Entry` as se WHERE se.name=stock.voucher_no)='Material Transfer for Manufacture',IF(stock.actual_qty>0,'26','27'),
										IF((SELECT title FROM `tabStock Entry` as se WHERE se.name=stock.voucher_no)='Manufacture',IF(stock.actual_qty>0,'19','10'),""))))),
						IF(stock.voucher_type='Purchase Receipt',(SELECT codigo_tipo_operacion FROM `tabPurchase Receipt` as pr WHERE pr.name=stock.voucher_no),
						IF(stock.voucher_type='Delivery Note',(SELECT codigo_tipo_operacion FROM `tabDelivery Note` as dn WHERE dn.name=stock.voucher_no),""))) as codigo_operacion,
					pro.item_name as descripcion_producto,
					pro.codigo_uom as uom,
					IF((SELECT value FROM `tabSingles` WHERE doctype='Stock Settings' AND field='valuation_method')='FIFO','2','1') as codigo_valuacion,
					IF(stock.actual_qty!=0,CAST(stock.actual_qty as DECIMAL(12,2)),'') as cantidad,
					IF(stock.actual_qty!=0,CAST(stock.valuation_rate as DECIMAL(12,2)),'0.00') as costo_unitario,
					IF(stock.actual_qty!=0,CAST(stock.stock_value as DECIMAL(12,2)),'0.00') as costo_total,
					IF(stock.actual_qty<0,CAST(stock.actual_qty as DECIMAL(12,2)),'0.00') as cantidad_retirado,
					IF(stock.actual_qty<0,CAST(stock.valuation_rate as DECIMAL(12,2)),'0.00') as costo_unitario_retirado,
					IF(stock.actual_qty<0,CAST(stock.stock_value as DECIMAL(12,2)),'0.00') as costo_total_retirado,
					IF(stock.qty_after_transaction,CAST(stock.qty_after_transaction as DECIMAL(12,2)),'') as saldo_final,
					IF(stock.stock_value,CAST(stock.stock_value as DECIMAL(12,2)),'') as costo_unitario_saldo_final,
					IF(stock.valuation_rate,CAST(stock.valuation_rate as DECIMAL(12,2)),'') as costo_total_saldo_final,
					'1' as anotacion
				from
					`tabStock Ledger Entry` as stock,
					`tabCompany` as comp,
					`tabItem` as pro
				where comp.name = stock.company
				and pro.name = stock.item_code
				and posting_date >= '""" + str(from_date) + """' 
				and posting_date <= '""" + str(to_date) + """' 
				order by posting_date""", as_dict=True)

		for d in inventories:
			inventory_list.append({
				'periodo': d.periodo,
				'cuo': d.cuo,
				'correlativo_asiento': d.correlativo_asiento,
				'almacen': d.almacen,
				'codigo_catalogo': d.codigo_catalogo,
				'codigo_tipo_existencia': d.codigo_tipo_existencia,
				'codigo_producto': d.codigo_producto,
				'codigo_sunat': d.codigo_sunat,
				'fecha_emision': d.fecha_emision,
				'codigo_comprobante': d.codigo_comprobante,
				'serie_comprobante': d.serie_comprobante,
				'correlativo_comprobante': d.correlativo_comprobante,
				'codigo_operacion': d.codigo_operacion,
				'descripcion_producto': d.descripcion_producto,
				'uom': d.uom,
				'codigo_valuacion': d.codigo_valuacion,
				'cantidad': d.cantidad,
				'costo_unitario': d.costo_unitario,
				'costo_total': d.costo_total,
				'cantidad_retirado': d.cantidad_retirado,
				'costo_unitario_retirado': d.costo_unitario_retirado,
				'costo_total_retirado': d.costo_total_retirado,
				'saldo_final': d.saldo_final,
				'costo_unitario_saldo_final': d.costo_unitario_saldo_final,
				'costo_total_saldo_final': d.costo_total_saldo_final,
				'anotacion': d.anotacion
			})
		return inventory_list

	def export_libro_inventario(self, year, periodo, ruc):
		tipo = "inventario"
		data = self.get_inventory(year, periodo)
		codigo_periodo = self.ple_name(year, periodo)
		nombre = "LE" + str(ruc) + codigo_periodo + '00130100' + '00' + '1' + ('1' if data else '0') + '1' + '1'
		nombre = nombre + ".txt"
		return to_file(data, tipo, nombre)
