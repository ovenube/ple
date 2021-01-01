# -*- coding: utf-8 -*-
# Copyright (c) 2015, seethersan and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import os
import frappe
import datetime

from platform import python_version
from pyreportjasper import PyReportJasper
from ple.ple_peru.utils import Utils

class ReportedeLibrosElectronicos(Utils):
	def make_report(self, year, periodo, tipo):
		from_date, to_date = self.get_dates(year, periodo)
		reporte = make_jasper_report("LE_"+ tipo, from_date, to_date, tipo)


def make_jasper_report(reporte, from_date, to_date, tipo):
	from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').strftime('%d/%m/%Y')
	to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').strftime('%d/%m/%Y')
	my_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
	my_path = os.path.abspath(os.path.join(my_path, os.pardir))
	input_file = os.path.dirname(my_path) + "/jasper_reports/" + reporte + ".jrxml"
	output = os.path.dirname(my_path) + '/reportes/' + tipo.lower() + "_" + str(datetime.datetime.now())
	con = {
		'driver': 'mysql',
		'username': frappe.conf.get("db_name"),
		'password': frappe.conf.get("db_password"),
		'host': frappe.conf.get("db_host"),
		'database': frappe.conf.get("db_name"),
		'port': '3306'
	}
	jasper = PyReportJasper()
	jasper.config(
        input_file,
        output_file=output,
        output_formats=["pdf", "rtf", "xml"],
        parameters={'from_date': from_date, 'to_date': to_date},
        db_connection=con,
        locale='en_US'  # LOCALE Ex.:(en_US, de_GE)
    )
	jasper.process_report()
	return output
