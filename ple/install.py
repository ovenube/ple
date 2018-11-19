# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
import frappe
import os.path
import distutils.dir_util


def after_install():
    import_data()
    create_dirs()

def import_data():
    my_path = os.path.abspath(os.path.dirname(__file__))
    my_path = os.path.join(my_path, "imports/")
    path = os.path.join(my_path, "tipos_de_comprobante.csv")
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=str(','))
        for idx, val in enumerate(reader):
            if idx == 0:
                continue  # If csv have first row with headers

            # Do something with your data
            doc = frappe.new_doc('Tipos de Comprobante')
            doc.codigo_tipo_comprobante = val[0]
            doc.nombre_tipo_comprobante = val[1]
            doc.descripcion_tipo_comprobante = val[2]
            doc.insert()

    path = os.path.join(my_path, "tipos_de_documento_de_identidad.csv")
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=str(','))
        for idx, val in enumerate(reader):
            if idx == 0:
                continue  # If csv have first row with headers

            # Do something with your data
            doc = frappe.new_doc('Tipos de Documento de Identidad')
            doc.codigo_tipo_documento = val[0]
            doc.descripcion_tipo_documento = val[1]
            doc.insert()

    path = os.path.join(my_path, "tipos_de_pago.csv")
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=str(','))
        for idx, val in enumerate(reader):
            if idx == 0:
                continue  # If csv have first row with headers

            # Do something with your data
            doc = frappe.new_doc('Tipos de Pago')
            doc.codigo_tipo_pago = val[0]
            doc.descripcion_tipo_pago = val[1]
            doc.insert()

def create_dirs():
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "libros")
    distutils.dir_util.mkpath(path)
    my_path = os.path.join(my_path, "libros/")
    path = os.path.join(my_path, "compras")
    distutils.dir_util.mkpath(path)
    path = os.path.join(my_path, "ventas")
    distutils.dir_util.mkpath(path)
    path = os.path.join(my_path, "diario")
    distutils.dir_util.mkpath(path)
    path = os.path.join(my_path, "mayor")
    distutils.dir_util.mkpath(path)
    path = os.path.join(my_path, "inventario")
    distutils.dir_util.mkpath(path)