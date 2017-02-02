#! -*- coding: UTF-8 -*-
from __future__ import absolute_import

import time
import base64
import pymongo
import xlsxwriter
from datetime import datetime
from celery import shared_task

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.core.files.storage import default_storage
from django.conf import settings
from django.core.mail import send_mail, EmailMessage

from registro import models as registro_models
from colector import settings as colector_settings

@shared_task
def generate_xls_report(id, email, email2):
    """
    Run Worker: celery worker -A colector  -l info
    Run workers on Background : celery multi start worker1 -A colector --pidfile="$ctp/colector/celery/%n%I.pid" --logfile="$ctp/colector/celery/%n%I.log"
    Kill Workers: ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9
    :param id: Form id
    :param email: Mail to send report
    :return: None
    """
    servidor = pymongo.MongoClient('localhost', 27017)
    database = servidor.colector
    filled_forms = database.filled_forms.find({'form_id': str(id)}).sort("_id", -1)

    # Si hay registros realizo preparo la respuesta http, iterating on filled_forms
    if filled_forms.count() != 0:
        rows = []  # rows array que contiene las filas de la tabla
        # Below f is a document (a record)

        workbook = xlsxwriter.Workbook('reporttq.xlsx')
        worksheet = workbook.add_worksheet()

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Add a number format for cells with money.
        money = workbook.add_format({'num_format': '$#,##0'})

        # Start from the first cell. Rows and columns are zero indexed.
        rownumber = 1
        col = 0
        for f in filled_forms:
            f["rows"]["MongoId"] = str(f["_id"])
            #Addin cols to report
            hini={}
            hini['label']='Hora Inicio'
            hini["value"]=f["rows"]["Hora Inicio"]
            f["responses"].append(hini)

            hfin={}
            hfin['label']='Hora Fin'
            hfin["value"]=f["rows"]["Hora Fin"]
            f["responses"].append(hfin)

            hsinc={}
            hsinc['label']='Sincronizado'
            hsinc["value"]=f["rows"]["Sincronizado"]
            f["responses"].append(hsinc)
            # rows.append(f["rows"])#list of records
            mongoid = str(f["_id"])

            row = f["rows"]
            formulario = registro_models.Formulario.objects.get(id=int(id))
            row['form_name'] = formulario.nombre
            row['form_description'] = formulario.descripcion
            for response in f["responses"]:
                if response['label'] == 'Hora Inicio' or response['label'] == 'Hora Fin':
                    cellvalue = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(response['value']))

                if response['label'] == 'Sincronizado':
                    cellvalue = response['value']

                if response['label'] == 'latitud' or response['label'] == 'longitud' \
                    or response['label'] == 'form_id' or response['label'] == 'form_description' \
                    or response['label'] == 'MongoId' \
                    or response['label'] == 'record_id' or response['label'] == 'colector_id':
                    continue
                # input_id=response['input_id']
                # entrada = Entrada.objects.get(id = int(input_id))
                # response['label']=entrada.nombre
                # response['tipo']=entrada.tipo
                if response['tipo'] == "1" or response['tipo'] == "2":
                    cellvalue = response['value'].upper()

                if response['tipo'] == "3" or response['tipo'] == "4" or response['tipo'] == "5":
                    try:
                        response_id = response['value']
                        respuesta = registro_models.Respuesta.objects.get(id=int(response_id))
                        cellvalue = respuesta.valor
                    except Exception, e:
                        cellvalue = "Op_" + response['value']

                if response['tipo'] == "7" or response['tipo'] == "8" or response['tipo'] == "9" or response[
                    'tipo'] == "10" or response['tipo'] == "11" or response['tipo'] == "12" or response[
                    'tipo'] == "13" or response['tipo'] == "15" or response['tipo'] == "17":
                    cellvalue = response['value']
                # FOTOS TIENEN UN TAG ADICIONAL A FOTOS Y DOCUMENTOS
                if response['tipo'] == "6":
                    # src='/home/andres/media/'+response['value']
                    # src='https://s3-us-west-2.amazonaws.com/colector.co/media/'+str(response.id)+'/'+response['value']
                    # fileext = response['value'].split("_.",1)[1]
                    fid, tagfoto, tipoarchivo, fechafoto, algo, fileext = response['value'].split('_')

                    src = settings.MEDIA_URL + str(response['input_id']) + '/' + response['value'] + fileext
                    static_url = settings.STATIC_URL
                    if response['label'] in row:
                        cellvalue = cellvalue + ' - ' + src
                    else:
                        cellvalue = src

                if response['tipo'] == "14" or response['tipo'] == "16":
                    # src='/home/andres/media/'+response['value']
                    # src='https://s3-us-west-2.amazonaws.com/colector.co/media/'+str(entrada.id)+'/'+response['value']
                    # fileext = response['value'].split("_.",1)[1]
                    fid, tipoarchivo, fechafoto, algo, fileext = response['value'].split('_')

                    src = settings.MEDIA_URL + str(response['input_id']) + '/' + response['value'] + fileext
                    static_url = settings.STATIC_URL
                    if response['label'] in row:
                        cellvalue = cellvalue + ' - ' + src
                    else:
                        cellvalue = src

                # Adjust the column width.
                worksheet.set_column(col, col, 30)
                #Escribo el encabezado
                if rownumber-1 == 0:
                    worksheet.write(rownumber-1, col, response['label'], bold)
                worksheet.write(rownumber, col, cellvalue)
                col += 1
            rownumber += 1
            col = 0

            rows.append(row)  # list of records

        workbook.close()


    # Connect to s3
    s3_file_name = "reporte.xlsx"

    conn = S3Connection(colector_settings.AWS_ACCESS_KEY_ID, colector_settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(colector_settings.AWS_STORAGE_BUCKET_NAME_REPORTS)
    k = Key(bucket)
    k.key = s3_file_name
    k.set_contents_from_filename('reporttq.xlsx')
    k.set_acl('public-read')

    files3 = default_storage.open('reporte.xlsx', 'w')
    # file_to_attach = open('reporttq.xlsx', 'r')


    # TODO Estoy muy convencido que esto no debe ir aquí, pero por lo pronto lo voy a dejar aquí
    flag_send_mail = True
    flag_send_as_link = True
    if flag_send_mail:
        if flag_send_as_link:
            send_mail(
                "Reporte Colector",
                "Por favor descargue su reporte desde esta url: http://%s.s3.amazonaws.com/%s" % (
                    colector_settings.AWS_STORAGE_BUCKET_NAME_REPORTS,
                    s3_file_name
                ),

                "Andres de Colector <andres@colector.co>",
                [email,email2],
                html_message="Por favor descargue su reporte desde <a href='http://%s.s3.amazonaws.com/%s'>esta url</a> " % (
                    colector_settings.AWS_STORAGE_BUCKET_NAME_REPORTS,
                    s3_file_name
                ),
            )
        else:
            email = EmailMessage(
                "Reporte Colector",
                "Adjunto le enviamos el archivo con su reporte",
                "Andres de Colector <andres@colector.co>",
                [email,email2],
            )
            file_to_attach = open('reporttq.xlsx', 'r')
            data = file_to_attach.read()

            email.attach('reporte.xlsx', data, 'application/vnd.ms-excel')
            email.send()




@shared_task
def send_record_email(id, email2, email3, responses):
    """
    Run Worker: celery worker -A colector  -l info
    Run workers on Background : celery multi start worker1 -A colector --pidfile="$ctp/colector/celery/%n%I.pid" --logfile="$ctp/colector/celery/%n%I.log"
    Kill Workers: ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9
    :param id: Form id
    :param email: Mail to send report
    :return: None
    """
    servidor = pymongo.MongoClient('localhost', 27017)
    database = servidor.colector

    rows = []  # rows array que contiene las filas de la tabla
    row = {}
    formulario = registro_models.Formulario.objects.get(id=int(id))
    row['form_name'] = formulario.nombre
    row['form_description'] = formulario.descripcion

    html_body='<ul>'
    for response in responses:
        # input_id=response['input_id']
        # entrada = Entrada.objects.get(id = int(input_id))
        # response['label']=entrada.nombre
        # response['tipo']=entrada.tipo
        if response['tipo'] == "1" or response['tipo'] == "2":
            html_body = html_body + '<li>' + response['label'] + ': ' + response['value'] + '</li>'
            
        if response['tipo'] == "3" or response['tipo'] == "4" or response['tipo'] == "5":
            try:
                response_id = response['value']
                respuesta = registro_models.Respuesta.objects.get(id=int(response_id))
                html_body = html_body + '<li>' + response['label'] + ': ' + respuesta.valor + '</li>'
            except Exception, e:
                html_body = html_body + '<li>Op_' + response['label'] + ': ' + response['value'] + '</li>'

        if response['tipo'] == "7" or response['tipo'] == "8" or response['tipo'] == "9" or response[
            'tipo'] == "10" or response['tipo'] == "11" or response['tipo'] == "12" or response[
            'tipo'] == "13" or response['tipo'] == "15" or response['tipo'] == "17":
            html_body = html_body + '<li>' + response['label'] + ': ' + response['value'] + '</li>'

        # # FOTOS TIENEN UN TAG ADICIONAL A FOTOS Y DOCUMENTOS
        # if response['tipo'] == "6":
        #     # src='/home/andres/media/'+response['value']
        #     # src='https://s3-us-west-2.amazonaws.com/colector.co/media/'+str(response.id)+'/'+response['value']
        #     # fileext = response['value'].split("_.",1)[1]
        #     fid, tagfoto, tipoarchivo, fechafoto, algo, fileext = response['value'].split('_')

        #     src = 'https://s3-us-west-2.amazonaws.com/colector.co/media/' + str(response['input_id']) + '/' + response['value'] + fileext
        #     static_url = settings.STATIC_URL
        #     if response['label'] in row:
        #         html_body = html_body + '<li>' + response['label'] + ': ' + row[response[
        #             'label']] + '<div style="float:left"><a class="thumb"><img id="' + src + '" width="50px" height="50px" src="' + src + '" /><p>' + tagfoto + '</p></a></div>' + '</li>'
        #     else:
        #         html_body = html_body + '<li>' + response['label'] + ': ' + '<div style="float:left"><a class="thumb"><img id="' + src + '" width="50px" height="50px" src="' + src + '"/><p>' + tagfoto + '</p></a></div>' + '</li>'

        # if response['tipo'] == "14" or response['tipo'] == "16":
        #     # src='/home/andres/media/'+response['value']
        #     # src='https://s3-us-west-2.amazonaws.com/colector.co/media/'+str(entrada.id)+'/'+response['value']
        #     # fileext = response['value'].split("_.",1)[1]
        #     fid, tipoarchivo, fechafoto, algo, fileext = response['value'].split('_')

        #     src = settings.MEDIA_URL + str(response['input_id']) + '/' + response['value'] + fileext
        #     static_url = settings.STATIC_URL
        #     if response['label'] in row:
        #         html_body = html_body + '<li>' + response['label'] + ': ' + row[response[
        #             'label']] + '<div style="float:left"><a class="thumb"><img id="' + src + '" width="50px" height="50px" src="' + src + '" /></a></div>' + '</li>'
        #     else:
        #         html_body = html_body + '<li>' + response['label'] + ': ' + '<div style="float:left"><a class="thumb"><img id="' + src + '" width="50px" height="50px" src="' + src + '" /></a></div>' + '</li>'

    html_body=html_body + '</ul>'

    flag_send_mail = True
    flag_send_as_link = True
    if flag_send_mail:
        if flag_send_as_link:
            send_mail(
                "Nuevo Registro " + formulario.nombre,
                "Consolidado de los datos registrados en "  + formulario.nombre,
                "Andres de Colector <andres@colector.co>",
                [email2],
                html_message="<p>Datos registrados: </p>" + html_body,
            )
            send_mail(
                "Nuevo Registro " + formulario.nombre,
                "Consolidado de los datos registrados en "  + formulario.nombre,
                "Andres de Colector <andres@colector.co>",
                [email3],
                html_message="<p>Datos registrados: </p>" + html_body,
            )
        else:
            email = EmailMessage(
                "Nuevo Registro " + formulario.nombre,
                "Consolidado de los datos registrados en "  + formulario.nombre,
                "Andres de Colector <andres@colector.co>",
                [email2,email3],
            )
            file_to_attach = open('reporttq.xlsx', 'r')
            data = file_to_attach.read()

            email.attach('reporte.xlsx', data, 'application/vnd.ms-excel')
            email.send()


    # response = HttpResponse(content_type='application/vnd.ms-excel')
    # response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
    # response.write(excelfilename)
# from boto.s3.connection import S3Connection
#
# conn = S3Connection('AWSACCESSKEY','AWSSECRECTACCESSKEY')
# bucket = conn.get_bucket('colector')
# for key in bucket.list():
#     print key.name.encode('utf-8')