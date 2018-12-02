# -*- coding: utf-8 -*-
# Copyright (c) 2018, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from ple.ple_peru.utils import Utils, to_file

class LibroElectronicoMayor(Utils):
	def get_account_mayor(self, year, periodo):
		account_list = []
		from_date, to_date = self.get_dates(year, periodo)

		account = frappe.db.sql("""select
					CONCAT(DATE_FORMAT(gl.posting_date,'%Y%m'),'00') as periodo,
					REPLACE(voucher_no, '-', '') as cuo,
					CONCAT('M', IF(voucher_type = 'Sales Invoice', 
					(SELECT 
						COUNT(name)
					FROM
						`tabGL Entry` as gl_1
					WHERE gl_1.voucher_no = gl.voucher_no
					AND SUBSTRING(gl_1.account, 1, 2) <= SUBSTRING(gl.account, 1, 2)),
					(SELECT 
						COUNT(name)
					FROM
						`tabGL Entry` as gl_1
					WHERE gl_1.voucher_no = gl.voucher_no
					AND SUBSTRING(gl_1.account, 1, 2) >= SUBSTRING(gl.account, 1, 2)))) as correlativo_asiento,
					SUBSTRING(gl.account,1,POSITION('-' in gl.account)-2) as codigo_asiento,
					"" as cuo_ue,
					"" as centro_costo,
					IF(gl.account_currency = 'SOL', 'PEN', gl.account_currency) as tipo_moneda,
					IF(voucher_type = 'Purchase Invoice',
											(select 
												IF(LENGTH(`codigo_tipo_documento`) = 1, CONCAT('0', `codigo_tipo_documento`), `codigo_tipo_documento`)
											from
												`tabPurchase Invoice`where name=voucher_no),
											(select 
												IF(LENGTH(`codigo_tipo_documento`) = 1, CONCAT('0', `codigo_tipo_documento`), `codigo_tipo_documento`) 
											from 
												`tabSales Invoice`
											where name=voucher_no)) as codigo_documento,
					IF(voucher_type = 'Purchase Invoice',
											(select 
												`tax_id`
											from
												`tabPurchase Invoice`where name=voucher_no),
											(select 
												`tax_id` 
											from 
												`tabSales Invoice`
											where name=voucher_no)) as tax_id,
					IF(voucher_type = 'Purchase Invoice',
											(select 
												codigo_comprobante 
											from
												`tabPurchase Invoice`where name=voucher_no),
											(select 
												codigo_comprobante 
											from 
												`tabSales Invoice`
											where name=voucher_no)) as codigo_comprobante,
					IF(voucher_type = 'Purchase Invoice',IFNULL(
											(select 
												bill_series 
											from 
												`tabPurchase Invoice`
											where name=voucher_no),''),
											SUBSTRING_INDEX(SUBSTRING_INDEX(voucher_no,'-',-2),'-',1)) as serie_comprobante,
					IF(voucher_type = 'Purchase Invoice',
											(select 
												bill_no
											from 
												`tabPurchase Invoice`
											where name=voucher_no), SUBSTRING_INDEX(SUBSTRING_INDEX(voucher_no,'-',-2),'-',-1)) as numero_comprobante,
					DATE_FORMAT(gl.posting_date,'%d/%m/%Y') as fecha_contable,
					DATE_FORMAT(gl.posting_date,'%d/%m/%Y') as fecha_vencimiento,
					DATE_FORMAT(gl.posting_date,'%d/%m/%Y') as fecha_emision,
					gl.remarks as glosa,
					'' as glosa_referencial,
					ROUND(gl.debit_in_account_currency, 2) as debe,
					ROUND(gl.credit_in_account_currency, 2) as haber,
					IF(voucher_type = 'Purchase Invoice',
						 CONCAT('080100&',
										(select
											CONCAT(DATE_FORMAT(IFNULL(bill_expiration_date,bill_date),'%Y%m'),'00&', REPLACE(voucher_no, '-', ''), '&','M2')
										from
											`tabPurchase Invoice` purchase_invoice
										left join
														`tabJournal Entry Account` journal_entry
										on journal_entry.reference_name = purchase_invoice.name
										where purchase_invoice.name=voucher_no)),
						 (IF(voucher_type = 'Sales Invoice', CONCAT('140100&',
										(select
											CONCAT(DATE_FORMAT(due_date,'%Y%m'),'00&', REPLACE(voucher_no, '-', ''),'&', 'M1')
										from
											`tabSales Invoice` sales_invoice
										left join
											`tabJournal Entry Account` journal_entry
												on journal_entry.reference_name = sales_invoice.name
												where sales_invoice.name=voucher_no)),''))) as estructurado,
					'1' as estado
				from 
					`tabGL Entry` gl
				where SUBSTRING(account,1,POSITION('-' in account)-1) > 100
				and posting_date > '""" + str(from_date) + """' 
				and posting_date < '""" + str(to_date) + """' 
				order by posting_date""", as_dict=True)

		for d in account:
			account_list.append({
				'periodo': d.periodo,
				'cuo': d.cuo,
				'correlativo_asiento': d.correlativo_asiento,
				'codigo_asiento': d.codigo_asiento,
				'cuo_ue': d.cuo_ue,
				'centro_costo': d.centro_costo,
				'tipo_moneda': d.tipo_moneda,
				'tipo_documento': d.codigo_documento,
				'tax_id': d.tax_id,
				'codigo_comprobante': d.codigo_comprobante,
				'serie_comprobante': d.serie_comprobante,
				'numero_comprobante': d.numero_comprobante,
				'fecha_contable': d.fecha_contable,
				'fecha_vencimiento': d.fecha_vencimiento,
				'fecha_emision': d.fecha_emision,
				'glosa': d.glosa,
				'glosa_referencial': d.glosa_referencial,
				'debe': d.debe,
				'haber': d.haber,
				'estructurado': d.estructurado,
				'estado': d.estado
			})
		return account_list

	def export_libro_mayor(self, year, periodo, ruc):
		tipo = "mayor"
		data = self.get_account_mayor(year, periodo)
		codigo_periodo = self.ple_name(year, periodo)
		nombre = "LE" + str(ruc) + codigo_periodo + '00060100' + '00' + '1' + '1' + '1' + '1'
		nombre = nombre + ".txt"
		return to_file(data, tipo, nombre)
