#! -*- coding: UTF-8 -*-
from __future__ import absolute_import

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
def generate_xls_report(id, email):
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
        for f in filled_forms:
            f["rows"]["MongoId"] = str(f["_id"])
            # rows.append(f["rows"])#list of records
            mongoid = str(f["_id"])

            ############ ESTO DEMUESTRA QUE SE PUEDE SIMPLIFICAR EL SERVICIO PARA SINCRONIZAR REGISTROS, ESTA CARGA SE PUEDE PASAR AQUI
            # ## LA OTRA FORMA DE HACERLO, ES CONSULTAR DIRECTAMENTE EL NODO ROWS
            row = f["rows"]
            formulario = registro_models.Formulario.objects.get(id=int(id))
            row['form_name'] = formulario.nombre
            row['form_description'] = formulario.descripcion
            for response in f["responses"]:
                # input_id=response['input_id']
                # entrada = Entrada.objects.get(id = int(input_id))
                # response['label']=entrada.nombre
                # response['tipo']=entrada.tipo
                if response['tipo'] == "1" or response['tipo'] == "2":
                    row[response['label']] = response['value'].upper()

                if response['tipo'] == "3" or response['tipo'] == "4" or response['tipo'] == "5":
                    try:
                        response_id = response['value']
                        respuesta = registro_models.Respuesta.objects.get(id=int(response_id))
                        row[response['label']] = respuesta.valor
                    except Exception, e:
                        row[response['label']] = "Op_" + response['value']

                if response['tipo'] == "7" or response['tipo'] == "8" or response['tipo'] == "9" or response[
                    'tipo'] == "10" or response['tipo'] == "11" or response['tipo'] == "12" or response[
                    'tipo'] == "13" or response['tipo'] == "15" or response['tipo'] == "17":
                    row[response['label']] = response['value']
                # FOTOS TIENEN UN TAG ADICIONAL A FOTOS Y DOCUMENTOS
                if response['tipo'] == "6":
                    # src='/home/andres/media/'+response['value']
                    # src='https://s3-us-west-2.amazonaws.com/colector.co/media/'+str(response.id)+'/'+response['value']
                    # fileext = response['value'].split("_.",1)[1]
                    fid, tagfoto, tipoarchivo, fechafoto, algo, fileext = response['value'].split('_')

                    src = settings.MEDIA_URL + str(response['input_id']) + '/' + response['value'] + fileext
                    static_url = settings.STATIC_URL
                    if response['label'] in row:
                        row[response['label']] = row[response[
                            'label']] + '<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="' + src + '" width="50px" height="50px" src="' + static_url + 'administrador/admin/dist/img/avatar.png" data-err-src="' + static_url + 'administrador/admin/dist/img/avatar.png"/><p>' + tagfoto + '</p></a></div>'
                    else:
                        row[response[
                            'label']] = '<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="' + src + '" width="50px" height="50px" src="' + static_url + 'administrador/admin/dist/img/avatar.png" data-err-src="' + static_url + 'administrador/admin/dist/img/avatar.png"/><p>' + tagfoto + '</p></a></div>'

                if response['tipo'] == "14" or response['tipo'] == "16":
                    # src='/home/andres/media/'+response['value']
                    # src='https://s3-us-west-2.amazonaws.com/colector.co/media/'+str(entrada.id)+'/'+response['value']
                    # fileext = response['value'].split("_.",1)[1]
                    fid, tipoarchivo, fechafoto, algo, fileext = response['value'].split('_')

                    src = settings.MEDIA_URL + str(response['input_id']) + '/' + response['value'] + fileext
                    static_url = settings.STATIC_URL
                    if response['label'] in row:
                        row[response['label']] = row[response[
                            'label']] + '<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="' + src + '" width="50px" height="50px" src="' + static_url + 'administrador/admin/dist/img/avatar.png" data-err-src="' + static_url + 'administrador/admin/dist/img/avatar.png"/></a></div>'
                    else:
                        row[response[
                            'label']] = '<div style="float:left"><a class="thumb"><img onClick="openMedia()" id="' + src + '" width="50px" height="50px" src="' + static_url + 'administrador/admin/dist/img/avatar.png" data-err-src="' + static_url + 'administrador/admin/dist/img/avatar.png"/></a></div>'

            rows.append(row)  # list of records

    # else:
    #     print 'NO HAY REGISTROS'
    #     data = {}
    #     data['response_code'] = '404'
    #     data['response_description'] = 'No hay registros'
    #     data['rows'] = []
    #     data['total'] = 0
    #     return HttpResponse(json.dumps(data, default=json_util.default), content_type='application/json')

    # Create a workbook and add a worksheet.
    exceltimestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    excelfilename = str(id) + '_' + str(exceltimestamp) + '.xlsx'

    workbook = xlsxwriter.Workbook('reporttq.xlsx')
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    # Add a number format for cells with money.
    money = workbook.add_format({'num_format': '$#,##0'})

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for record in rows:
        for recordnode in record:
            if recordnode == 'latitud' or recordnode == 'longitud' \
                    or recordnode == 'form_id' or recordnode == 'form_description' \
                    or recordnode == 'MongoId' or recordnode == 'Hora Inicio' or recordnode == 'Hora Fin' \
                    or recordnode == 'record_id' or recordnode == 'sincronizado_utc' or recordnode == 'colector_id':
                continue
            # Adjust the column width.
            worksheet.set_column(col, col, 30)
            if row == 0:
                worksheet.write(row, col, recordnode, bold)
                col += 1
            else:
                worksheet.write(row, col, record[recordnode])
                col += 1
        row += 1
        col = 0

    # Write a total using a formula.
    # worksheet.write(row, 0, 'Total')
    # worksheet.write(row, 1, '=SUM(B1:B4)')

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
                "andres@colector.co",
                [email],
                html_message="Por favor descargue su reporte desde <a href='http://%s.s3.amazonaws.com/%s'>esta url</a> " % (
                    colector_settings.AWS_STORAGE_BUCKET_NAME_REPORTS,
                    s3_file_name
                ),
            )
        else:
            email = EmailMessage(
                "Reporte Colector",
                "Adjunto le enviamos el archivo con su reporte",
                "andres@colector.co",
                [email],
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