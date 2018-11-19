# -*- coding: utf-8 -*-
# Copyright (c) 2018, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from ple.ple_peru.utils import Utils, to_file

class LibroElectronicoMayor(Utils):
	def get_account(self, year, periodo):
		account_list = []
		from_date, to_date = self.get_dates(year, periodo)
		sales, purchase = self.get_series()


		account = frappe.db.sql("""select
				CONCAT(DATE_FORMAT(gl.posting_date,'%Y%m'),'00') as periodo,
				SUBSTRING(IF(gl.voucher_no like 'JV%',gl.voucher_no,
									(select 
										min(voucher_no) 
									from 
										`tabGL Entry`
									where against_voucher=gl.voucher_no and voucher_no like 'JV%')),4) as cuo,
				CONCAT('M',IF(voucher_no like 'JV%','2','1')) as correlativo_asiento,
				SUBSTRING(gl.against,1,POSITION('-' in gl.against)-2) as codigo_asiento,
				SUBSTRING(IF(gl.voucher_no like 'JV%',gl.voucher_no,
									(select 
										min(voucher_no) 
									from 
										`tabGL Entry`
									where against_voucher=gl.voucher_no and voucher_no like 'JV%')),4) as cuo_ue,
				"" as centro_costo,
				gl.account_currency as tipo_moneda,
				(select 
					codigo_tipo_documento
				from 
					`tabCompany` 
				where company_name=company) as tipo_documento,
				(select 
					tax_id 
				from 
					`tabCompany` 
				where company_name=company) as tipo_documento,
				IF(against_voucher like '""" + purchase + """',
										(select 
											codigo_tipo_comprobante 
										from
											`tabPurchase Invoice`where name=against_voucher),
										(select 
											codigo_comprobante 
										from 
											`tabSales Invoice`
										where name=against_voucher)) as codigo_comprobante,
				IF(against_voucher like '""" + purchase + """',IFNULL(
										(select 
											bill_series 
										from 
											`tabPurchase Invoice`
										where name=against_voucher),''),
										SUBSTRING(against_voucher,4,3)) as serie_comprobante,
				IF(against_voucher like '""" + purchase + """',
										(select 
											bill_no
										from 
											`tabPurchase Invoice`
										where name=against_voucher), SUBSTRING(against_voucher,8)) as numero_comprobante,
				DATE_FORMAT(gl.posting_date,'%d/%m/%Y') as fecha_contable,
				DATE_FORMAT(gl.posting_date,'%d/%m/%Y') as fecha_vencimiento,
				DATE_FORMAT(gl.posting_date,'%d/%m/%Y') as fecha_emision,
				gl.remarks as glosa,
				gl.debit_in_account_currency as debe,
				gl.credit_in_account_currency as haber,
				IF(against_voucher like '""" + purchase + """',
					 CONCAT('080100',
									(select
										CONCAT(DATE_FORMAT(IFNULL(bill_expiration_date,bill_date),'%Y%m'),'00', SUBSTRING(journal_entry.parent,4), CONCAT('M',journal_entry.idx))
									from
										`tabPurchase Invoice` purchase_invoice
									left join
													`tabJournal Entry Account` journal_entry
									on journal_entry.reference_name = purchase_invoice.name
									where purchase_invoice.name=against_voucher)),
					 (IF(against_voucher like '""" + sales + """', CONCAT('140100',
									(select
										CONCAT(DATE_FORMAT(due_date,'%Y%m'),'00', IFNULL(SUBSTRING(journal_entry.parent,4),'0'), IFNULL(CONCAT('M',journal_entry.idx),'M1'))
									from
										`tabSales Invoice` sales_invoice
									left join
										`tabJournal Entry Account` journal_entry
											on journal_entry.reference_name = sales_invoice.name
											where sales_invoice.name=against_voucher)),''))) as estructurado,
				'1' as estado
			from 
				`tabGL Entry` gl
			where SUBSTRING(against,1,POSITION('-' in against)-1) > 100
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
				'tipo_documento': d.tipo_documento,
				'codigo_comprobante': d.codigo_comprobante,
				'serie_comprobante': d.serie_comprobante,
				'numero_comprobante': d.numero_comprobante,
				'fecha_contable': d.fecha_contable,
				'fecha_emision': d.fecha_emision,
				'fecha_vencimiento': d.fecha_vencimiento,
				'glosa': d.glosa,
				'debe': d.debe,
				'haber': d.haber,
				'estructurado': d.estructurado,
				'estado': d.estado
			})
		return account_list

	def export_libro_mayor(self, year, periodo, ruc):
		tipo = "mayor"
		data = self.get_account(year, periodo)
		codigo_periodo = self.ple_name(year, periodo)
		nombre = "LE" + str(ruc) + codigo_periodo + '00060100' + '00' + '1' + '1' + '1' + '1'
		nombre = nombre + ".txt"
		return to_file(data, tipo, nombre)
