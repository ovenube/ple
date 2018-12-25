# -*- coding: utf-8 -*-
# Copyright (c) 2015, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from ple.ple_peru.utils import Utils, to_file


class LibroElectronicoDiario(Utils):
	def get_account(self, year, periodo, primer=None):
		account_list = []
		from_date, to_date = self.get_dates(year, periodo)

		if primer == "1":
			account = frappe.db.sql("""select
					DATE_FORMAT(NOW(),'%Y%m%d') as periodo,
					SUBSTRING(name,1,POSITION('-' in name)-2) as codigo_asiento,
					SUBSTRING(name,POSITION('-' in name)+2) as descripcion_asiento,
					'01' as codigo_plan,
					'PLAN CONTABLE GENERAL EMPRESARIAL' as descripcion_plan,
					"" as codigo_cuenta,
					"" as descripcion_cuenta,
					'1' as indicador_cuenta
				from
					`tabAccount`
				where SUBSTRING(name,1,POSITION('-' in name)-1) > 100""", as_dict=True)

			for d in account:
				account_list.append({
					'periodo': d.periodo,
					'codigo_asiento': d.codigo_asiento,
					'descripcion_asiento': d.descripcion_asiento,
					'codigo_plan': d.codigo_plan,
					'descripcion_plan': d.descripcion_plan,
					'codigo_cuenta': d.codigo_cuenta,
					'descripcion_cuenta': d.descripcion_cuenta,
					'indicador_cuenta': d.indicador_cuenta
				})
		else:
			account = frappe.db.sql("""select
					IF(voucher_type = 'Purchase Invoice', '02', IF(voucher_type = 'Sales Invoice', '01', '03')) as origen,
					(SELECT
						COUNT(name)
					FROM 
						`tabGL Entry` as gl_1
					WHERE SUBSTRING(gl_1.name,3) <= SUBSTRING(gl.name,3)) nro_voucher,
					DATE_FORMAT(gl.posting_date,'%d/%m/%Y') as fecha,
					SUBSTRING(gl.account,1,POSITION('-' in gl.account)-2) as codigo_asiento,
					IF(gl.debit_in_account_currency = 0, '0.00', ROUND(gl.debit_in_account_currency, 2)) as debe,
					IF(gl.credit_in_account_currency = 0, '0.00', ROUND(gl.credit_in_account_currency, 2)) as haber,
					IF(gl.account_currency = 'SOL' OR 'PEN', 'S', 'D') as moneda,
					IFNULL(IF(voucher_type = 'Purchase Invoice',
											(select 
												conversion_rate
											from
												`tabPurchase Invoice`where name=voucher_no),
											(select 
												conversion_rate
											from 
												`tabSales Invoice`
											where name=voucher_no)),'1.000') as tipo_cambio,
					IF(voucher_type = 'Purchase Invoice',
											(select 
												IF(LENGTH(codigo_comprobante) = 1, CONCAT('0', codigo_comprobante), codigo_comprobante)
											from
												`tabPurchase Invoice`where name=voucher_no),
					IF(voucher_type = 'Sales Invoice',
											(select 
												IF(LENGTH(codigo_comprobante) = 1, CONCAT('0', codigo_comprobante), codigo_comprobante) 
											from 
												`tabSales Invoice`
											where name=voucher_no),
					IF(voucher_type = 'Delivery Note', (select 
												IF(LENGTH(codigo_tipo_comprobante) = 1, CONCAT('0', codigo_tipo_comprobante), codigo_tipo_comprobante) 
											from 
												`tabDelivery Note`
											where name=voucher_no),
					IF(voucher_type = 'Purchase Receipt', (select 
												IF(LENGTH(codigo_tipo_comprobante) = 1, CONCAT('0', codigo_tipo_comprobante), codigo_tipo_comprobante) 
											from 
												`tabPurchase Receipt`
											where name=voucher_no),'')))) as codigo_comprobante,
					CONCAT(IF(voucher_type = 'Purchase Invoice',IFNULL(
											(select 
												bill_series 
											from 
												`tabPurchase Invoice`
											where name=voucher_no),''),
											SUBSTRING_INDEX(SUBSTRING_INDEX(voucher_no,'-',-2),'-',1)),'-',
					IF(voucher_type = 'Purchase Invoice',
											(select 
												bill_no
											from 
												`tabPurchase Invoice`
											where name=voucher_no), SUBSTRING_INDEX(SUBSTRING_INDEX(voucher_no,'-',-2),'-',-1))) as numero_comprobante,
					DATE_FORMAT(gl.posting_date,'%d/%m/%Y') as fechad,
					IFNULL(IF(voucher_type = 'Purchase Invoice',
											(select 
												DATE_FORMAT(due_date,'%d/%m/%Y')
											from
												`tabPurchase Invoice`where name=voucher_no),
											(select 
												DATE_FORMAT(due_date,'%d/%m/%Y')
											from 
												`tabSales Invoice`
											where name=voucher_no)),DATE_FORMAT(gl.posting_date,'%d/%m/%Y')) as fechav,
					IFNULL(IF(voucher_type = 'Purchase Invoice',
											(select 
												`tax_id`
											from
												`tabPurchase Invoice`where name=voucher_no),
											(select 
												`tax_id` 
											from 
												`tabSales Invoice`
											where name=voucher_no)),'') as tax_id,
					IFNULL(gl.cost_center,'') as centro_costo,
					'' as codigo_financiero,
					'' as presupuesto,
					IF(voucher_type = 'Payment Entry', 
						(SELECT
							IF(mode_of_payment = "Cheque", '007',
								IF(mode_of_payment = "Efectivo", '008',
									IF(mode_of_payment = "Transferencia bancaria", '003',
										IF(mode_of_payment = "Giro Bancario", '002',''))))
						FROM 
							`tabPayment Entry` as pe
						WHERE pe.name = gl.voucher_no), '') as tipo_pago,
					gl.remarks as glosa,
					IF(SUBSTRING(gl.voucher_no,0,2)='ND' OR 'NC',voucher_no,'') as ref_nota,
					IF(SUBSTRING(gl.voucher_no,0,2)='ND','08',IF(SUBSTRING(gl.voucher_no,0,2)='NC','07','')) as tipo_nota,
					IF(SUBSTRING(gl.voucher_no,0,2)='ND' OR 'NC',DATE_FORMAT(gl.posting_date,'%d/%m/%Y'),'') as fecha_nota,
					'' as numero_detrac,
					'' as fecha_detrac,
					IF(voucher_type='Purchase Invoice','C',IF(voucher_type='Sales Invoice','V')) as tl,
					
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

	def export_libro_diario(self, year, periodo, ruc, primer):
		tipo = "diario"
		data = self.get_account(year, periodo, primer)
		codigo_periodo = self.ple_name(year, periodo)
		if primer == "1":
			nombre = "LE" + str(ruc) + codigo_periodo + '00050300' + '00' + '1' + '1' + '1' + '1'
		else:
			nombre = "LE" + str(ruc) + codigo_periodo + '00050100' + '00' + '1' + '1' + '1' + '1'
		nombre = nombre + ".txt"
		return to_file(data, tipo, nombre, primer)
