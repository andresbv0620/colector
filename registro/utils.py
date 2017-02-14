#! -*- coding: utf-8 -*-
import csv
import codecs
from django.core import serializers
# =============== Funciones para leer CSV formato UTF - 8 ===============


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    """
    Lector de datos csv
    :param unicode_csv_data: Datos del archivo CSV
    :param dialect: Dialecto del CSV
    :param kwargs: Otros argumentos
    :return: Iterador para el recorrido sobre los archivos
    """
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(
        utf_8_encoder(unicode_csv_data),
        dialect=dialect,
        **kwargs
    )
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    """
    Codificador URF-8
    :param unicode_csv_data: Archivo unicode
    :return: Iterador que recorrerá el archivo y lo codificará a UTF-8
    """
    for line in unicode_csv_data:
        yield line.encode('utf-8')


# ============== Extraer dependientes de TQ ===================


def extract_tq_dependientes(path):
    """
    Dado un archivo proveido por tecnoquímicas, extraer la información necesaria estructurada en un arbol de dependencias
    Para usar desde consola.
    Uso:
from registro import utils
a,b,c,d = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_simple.csv')
    :param path: Ruta del archivo TQ en formato CSV
    :return: a: Arbol de información, Lista con Representantes, Lista con Farmacias y Lista con Dependientes
    """
    archivo = codecs.open(path, 'r', encoding="utf-8", errors='ignore')
    lineas = archivo.readlines()
    reader = unicode_csv_reader(lineas)
    line = 0
    ids_representantes = []
    representantes = []
    ids_farmacias = []
    farmacias = []
    ids_dependientes = []
    dependientes = []

    arbol = dict()
    for r in reader:
        print line
        line += 1
        if line == 1:
            continue
        if not r[2] in ids_representantes:
            ids_representantes.append(r[2])
            representantes.append(extraer_representante(r))
            arbol[r[2]] = dict()
            arbol[r[2]]['farmacias'] = []
        print arbol
        ubicacion_farmacia = buscar_en_arreglo(r[4], arbol[r[2]]['farmacias'])
        if ubicacion_farmacia == -1:
            ubicacion_farmacia = len(arbol[r[2]]['farmacias'])
            farmacias.append(extraer_farmacia(r))
            arbol[r[2]]['farmacias'].append({'id': r[4], 'dependientes': []})
        print arbol
        ubicacion_dependiente = buscar_en_arreglo(r[7], arbol[r[2]]['farmacias'][ubicacion_farmacia]['dependientes'])
        if ubicacion_dependiente == -1:
            dependientes.append(extraer_dependiente(r))
            arbol[r[2]]['farmacias'][ubicacion_farmacia]['dependientes'].append({'id': r[7]})
        print arbol

    return (
        arbol,
        representantes,
        farmacias,
        dependientes
    )


def buscar_en_arreglo(id, arreglo):
    """
    Busca información en una lista de la con elementos cuyo id estén en un diccionario con llave id
    :param id: índice a buscar
    :param arreglo: lista con elementos de la forma {'id': int, .....}
    :return: índice en la lista si se encuentra, -1 si no
    """
    i = 0
    for x in arreglo:
        if id == x['id']:
            return i
        i += 1
    return -1


def extraer_representante(r):
    """
    Dada una fila de un archivo CSV extrae la información de un Representante
    :param r: Fila de archivo CSV
    :return: Representante
    """
    representante = dict()
    representante['id'] = r[2]
    representante['nombre'] = r[3]
    return representante


def extraer_farmacia(r):
    """
    Dada una fila de un archivo CSV extrae la información de un Farmacia
    :param r: Fila de archivo CSV
    :return: Farmacia
    """
    farmacia = dict()
    farmacia['id'] = r[4]
    farmacia['nombre'] = r[6]
    farmacia['codigo_tq'] = r[5]
    farmacia['ciudad'] = r[1]
    farmacia['departamento'] = r[0]
    return farmacia


def extraer_dependiente(r):
    """
    Dada una fila de un archivo CSV extrae la información de un dependiente
    :param r: Fila de archivo CSV
    :return: Dependiente
    """
    dependiente = dict()
    dependiente['id'] = r[7]
    dependiente['tipoDocumento'] = r[8]
    dependiente['documento'] = r[9]
    dependiente['habeas_data'] = r[10]
    dependiente['cedula_validada'] = r[11]
    dependiente['nombres'] = r[12]
    dependiente['apellidos'] = r[13]
    dependiente['fecha_nacimiento'] = r[14]
    dependiente['genero'] = r[15]
    dependiente['estado_civil'] = r[16]
    dependiente['email'] = r[17]
    dependiente['telefono_fijo'] = r[18]
    dependiente['telefono_celular'] = r[19]
    dependiente['telefono_farmacia'] = r[20]
    dependiente['tecnico_auxiliar'] = r[21]
    dependiente['hijos'] = r[22]
    dependiente['parentezco_familiar'] = r[23]
    dependiente['nombre_familiar'] = r[24]
    dependiente['nacimiento_familiar'] = r[25]
    dependiente['sexo_familiar'] = r[26]

    return dependiente


# ============ Obtener todo lo relacionado con un formulario ===========

def extracer_formulario(id):
    """
    Extrae toda la información de un formulario dado su ID
    Uso:
from registro import utils
a,b,c,d,e = utils.extracer_formulario(1)
    :param id: Identificador del formulario
    :return: Información serializada del formulario
    """
    from . import models

    formulario = models.Formulario.objects.filter(pk=id)

    formulario_serializado = serializers.serialize('json', formulario)

    fichas_serializadas = []
    entradas_serializadas = []
    asignacion_entradas_serializadas = []
    respuestas_serializadas = []

    if formulario.count() > 0:
        fichas = formulario[0].ficha.all()

        fichas_serializadas = serializers.serialize('json', fichas)
        entradas_ids = []
        for ficha in fichas:
            entradas_ids.extend([x.id for x in ficha.entrada.all()])
        entradas = models.Entrada.objects.filter(id__in=entradas_ids)
        entradas_serializadas = serializers.serialize('json', entradas)
        asignacion_entradas = models.AsignacionEntrada.objects.filter(entrada__id__in=entradas_ids)
        asignacion_entradas_serializadas = serializers.serialize('json', asignacion_entradas)
        respuestas_ids = []
        for entrada in entradas:
            respuestas_ids.extend([x.id for x in entrada.respuesta.all()])
        respuestas = models.Respuesta.objects.filter(id__in=respuestas_ids)
        respuestas_serializadas = serializers.serialize('json', respuestas)

    return (
        formulario_serializado,
        fichas_serializadas,
        entradas_serializadas,
        asignacion_entradas_serializadas,
        respuestas_serializadas
    )


def guardar_tupla_archivo(path, tupla):
    """
    Guarda una tupla en un archivo, util para extraer la información d eun formulario a un archivo plano
    Uso:
from registro import utils
utils.guardar_tupla_archivo('data.json', utils.extracer_formulario(1))
    :param path: Ruta del archivo a guardar
    :param tupla: Una tupla cualquiera
    :return: None
    """
    archivo = codecs.open(path, "w+")
    for elemento in tupla:
        archivo.write("%s\n" % elemento)
    archivo.close()

def guardar_archivo_serializado_base_de_datos(path):
    """
    Guarda el contenido de un archivo en la base de datos si el contenido está serializado
from registro import utils
utils.guardar_archivo_serializado_base_de_datos('data.json')
    :param path:  Ruta del archivo con los datos serializados
    :return: None
    """
    archivo = codecs.open(path, "r")
    lineas = archivo.readlines()
    for linea in lineas:
        print(linea)
        for deserialized_object in serializers.deserialize('json', linea):
            deserialized_object.save()
    archivo.close()