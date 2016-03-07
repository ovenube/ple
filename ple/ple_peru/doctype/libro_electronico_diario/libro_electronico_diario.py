# -*- coding: utf-8 -*-
# Copyright (c) 2015, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from ple.ple_peru.utils import send_txt_to_client

class LibroElectronicoDiario(Document):
	pass

@frappe.whitelist()
def get_account(year, periodo, primer=None):
	account_list = []
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

	if primer=="1":
		account = frappe.db.sql("""select
				DATE_FORMAT(NOW(),'%Y%m%d') as periodo,
				SUBSTRING(account_name,1,POSITION('-' in name)-2) as codigo_asiento,
				SUBSTRING(account_name,POSITION('-' in name)+2) as descripcion_asiento,
				'01' as codigo_plan,
				'PLAN CONTABLE GENERAL EMPRESARIAL' as descripcion_plan,
				"" as codigo_cuenta,
				"" as descripcion_cuenta,
				'1' as indicador_cuenta
			from
				`tabAccount`
			where SUBSTRING(account_name,1,POSITION('-' in name)-1) > 100""", as_dict=True)

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
				CONCAT(DATE_FORMAT(gl.posting_date,'%Y%m'),'00') as periodo,
		        SUBSTRING(IF(gl.voucher_no like 'JV%',gl.voucher_no,(select min(voucher_no) from `tabGL Entry` 
		        					where against_voucher=gl.voucher_no and voucher_no like 'JV%')),4) as cuo,
		        CONCAT('M',IF(voucher_no like 'JV%','2','1')) as correlativo_asiento,
		        SUBSTRING(gl.against,1,POSITION('-' in gl.against)-2) as codigo_asiento,
		        SUBSTRING(IF(gl.voucher_no like 'JV%',gl.voucher_no,(select min(voucher_no) from `tabGL Entry` 
		        					where against_voucher=gl.voucher_no and voucher_no like 'JV%')),4) as cuo_ue,
		        "" as centro_costo,
		        gl.account_currency as tipo_moneda,
		        (select codigo_tipo_documento from `tabCompany` where company_name=company) as tipo_documento,
		        (select tax_id from `tabCompany` where company_name=company) as tipo_documento,
		        IF(against_voucher like 'PINV%',(select codigo_tipo_comprobante from 
		        								`tabPurchase Invoice`where name=against_voucher),
												(select codigo_comprobante from `tabSales Invoice` 
												where name=against_voucher)) as codigo_comprobante,
		        IF(against_voucher like 'PINV%',IFNULL((select bill_series from `tabPurchase Invoice` 
		        								where name=against_voucher),''),
												SUBSTRING(against_voucher,4,3)) as serie_comprobante,
		        IF(against_voucher like 'PINV%',(select bill_no from `tabPurchase Invoice`where name=against_voucher),
		        								SUBSTRING(against_voucher,8)) as numero_comprobante,
		        DATE_FORMAT(gl.posting_date,'%d/%m/%Y') as fecha_contable,
		        DATE_FORMAT(gl.posting_date,'%d/%m/%Y') as fecha_vencimiento,
		        DATE_FORMAT(gl.posting_date,'%d/%m/%Y') as fecha_emision,
		        gl.remarks as glosa,
		        gl.debit_in_account_currency as debe,
		        gl.credit_in_account_currency as haber,
		        IF(against_voucher like 'PINV%','080100',(IF(against_voucher like 'BV%','140100',''))) as estructurado,
		        '1' as estado
			from 
				`tabGL Entry` gl
			where SUBSTRING(against,1,POSITION('-' in against)-1) > 100
			and posting_date > '"""+str(from_date)+"""' 
			and posting_date < '"""+str(to_date)+"""' 
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


@frappe.whitelist()
def export_libro_diario(year, periodo, ruc, primer):
	tipo = "diario"
	codigo_periodo = ""
	data = get_account(year, periodo, primer)
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
	if primer=="1":
		nombre = "LE"+str(ruc)+codigo_periodo+'050300'+'00'+'1'+'1'+'1'+'1'
	else:
		nombre = "LE"+str(ruc)+codigo_periodo+'050100'+'00'+'1'+'1'+'1'+'1'
	send_txt_to_client(data, nombre, tipo, primer)
