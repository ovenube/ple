# -*- coding: utf-8 -*-
# Copyright (c) 2015, seethersan and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
import frappe.desk.reportview

from ple.ple_peru.utils import Utils, to_file


class LibroElectronicodeVentas(Utils):
    def get_sales_invoices(self, year, periodo):
        sales_invoice_list = []
        from_date, to_date = self.get_dates(year, periodo)

        sales_invoices = frappe.db.sql("""select
				CONCAT(DATE_FORMAT(posting_date,'%Y%m'),'00') as periodo,
				REPLACE(sales_invoice.name, '-', '') as cuo,
				'M1' as correlativo_asiento,
				DATE_FORMAT(posting_date,'%d/%m/%Y') as fecha_emision,
				DATE_FORMAT(posting_date,'%d/%m/%Y') as fecha_cancelacion,
				IF(LENGTH(codigo_comprobante) = 1,CONCAT('0',codigo_comprobante), codigo_comprobante) as tipo_comprobante,
				SUBSTRING(sales_invoice.name,4,4) as serie_comprobante,
				SUBSTRING(sales_invoice.name,9) as numero_comprobante,
				"" as resumen_diario,
				IF(base_net_total>700,codigo_tipo_documento,IF(ISNULL(tax_id),"",IFNULL(codigo_tipo_documento,""))) as tipo_documento,
				IF(codigo_tipo_documento=7,IF(SUBSTRING(REPLACE(tax_id,"-",""),-12)="",tax_id, SUBSTRING(REPLACE(tax_id,"-",""),-12)),IF(base_net_total>700,tax_id,IF(ISNULL(tax_id),"",tax_id))) as numero_documento,
				IF(base_net_total>700,customer_name,IF(ISNULL(tax_id),"",IF(customer_name='Clientes Varios',customer_boleta_name,customer_name))) as nombre_cliente,
				"" as valor_exportacion,
				ROUND(base_net_total, 2) as base_imponible,
				"" as descuento,
				ROUND(base_total_taxes_and_charges, 2) as monto_impuesto,
				"" as descuento_igv,
				"" as total_exonerado,
				"" as total_inafecto,
				"" as monto_isc,
				"" as base_arroz,
				"" as impuesto_arroz,
				"" as otros_conceptos,
				ROUND(base_grand_total, 2) as valor_adquisicion,
				IF(currency = 'SOL', 'PEN', currency) as moneda,
				SUBSTRING(conversion_rate,1,POSITION('.' in conversion_rate)+3) as tipo_cambio,
				IF(is_return,(SELECT DATE_FORMAT(sales_return.posting_date,'%d/%m/%Y') FROM `tabSales Invoice` as sales_return WHERE sales_return.name=sales_invoice.return_against),"") as fecha_inicial_devolucion,
				IF(is_return,(SELECT sales_return.codigo_comprobante FROM `tabSales Invoice` as sales_return WHERE sales_return.name=sales_invoice.return_against),"") as tipo_devolucion,
				IF(is_return,SUBSTRING((SELECT sales_return.name FROM `tabSales Invoice` as sales_return WHERE sales_return.name=sales_invoice.return_against),4,4),"") as serie_devolucion,
				IF(is_return,SUBSTRING((SELECT sales_return.name FROM `tabSales Invoice` as sales_return WHERE sales_return.name=sales_invoice.return_against),9),"")  as numero_devolucion,
				"" as contrato,
				"" as error_1,
				'1' as indicador_pago,
				IF(sales_invoice.docstatus='2','2',IF(CONCAT(DATE_FORMAT(posting_date,'%Y-%m'),'-01')>=posting_date,'7','1')) as anotacion
			from
				`tabSales Invoice` as sales_invoice
			where posting_date  >= '""" + str(from_date) + """' 
			and posting_date  <= '""" + str(to_date) + """'
            and docstatus != 0
			order by posting_date""", as_dict=True)

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
                'numero_devolucion': d.numero_devolucion,
                'contrato': d.contrato,
                'error_1': d.error_1,
                'indicador_pago': d.indicador_pago,
                'anotacion': d.anotacion
            })
        return sales_invoice_list

    def export_libro_ventas(self, year, periodo, ruc):
        tipo = "ventas"
        data = self.get_sales_invoices(year, periodo)
        codigo_periodo = self.ple_name(year, periodo)
        nombre = "LE" + str(ruc) + codigo_periodo + '00140100' + '00' + '1' + ('1' if data else '0') + '1' + '1'
        nombre = nombre + ".txt"
        return to_file(data, tipo, nombre)
