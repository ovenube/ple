# -*- coding: utf-8 -*-
# Copyright (c) 2015, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from ple.ple_peru.doctype.libro_electronico_de_compras.libro_electronico_de_compras import LibroElectronicodeCompras
from ple.ple_peru.doctype.libro_electronico_de_ventas.libro_electronico_de_ventas import LibroElectronicodeVentas
from ple.ple_peru.doctype.libro_electronico_diario.libro_electronico_diario import LibroElectronicoDiario
from ple.ple_peru.doctype.libro_electronico_mayor.libro_electronico_mayor import LibroElectronicoMayor
from ple.ple_peru.utils import to_file

class ReportedeLibrosElectronicos(LibroElectronicodeVentas, LibroElectronicodeCompras, LibroElectronicoDiario, LibroElectronicoMayor):
	def get_data(self, year, periodo, tipo):
		if tipo == "Ventas":
			return self.get_sales_invoices(year, periodo)
		elif tipo == "Compras":
			return self.get_purchase_invoices(year, periodo)
		elif tipo == "Diario":
			return self.get_account(year, periodo)
		elif tipo == "Mayor":
			return self.get_account_mayor(year, periodo)

	def export_reporte_libros(self, year, periodo, tipo):
		codigo_periodo = ""
		data = self.get_data(year, periodo, tipo)
		nombre = "Libro Electronico de " + tipo + " - " + codigo_periodo + ".csv"
		to_file(data, nombre, tipo)

