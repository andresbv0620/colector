#! -*- coding: utf-8 -*-
import csv
import codecs
from django.core import serializers
# =============== Funciones para leer CSV formato UTF - 8 ===============

PREGUNTA_FARMACIA = 997
PREGUNTA_DEPENDIENTE = 998


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
a,b,c,d = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ultra_simple.csv')
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
        # print line
        line += 1
        if line < 3:
            continue
        if not r[2] in ids_representantes:
            ids_representantes.append(r[2])
            representantes.append(extraer_representante(r))
            arbol[r[2]] = []
            # arbol[r[2]]['farmacias'] = []
        # print arbol
        ubicacion_farmacia = buscar_en_arreglo(r[4], arbol[r[2]])
        if ubicacion_farmacia == -1:
            ubicacion_farmacia = len(arbol[r[2]])
            farmacias.append(extraer_farmacia(r))
            arbol[r[2]].append({'id': r[4], 'dependientes': []})
        # print arbol
        ubicacion_dependiente = buscar_en_arreglo(r[7], arbol[r[2]][ubicacion_farmacia]['dependientes'])
        if ubicacion_dependiente == -1:
            dependientes.append(extraer_dependiente(r))
            arbol[r[2]][ubicacion_farmacia]['dependientes'].append({'id': r[7]})
        # print arbol

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
    # farmacia['nombre'] = r[6]
    # farmacia['codigo_tq'] = r[5]
    farmacia['1000'] = r[1]
    farmacia['999'] = r[0]
    return farmacia


def extraer_dependiente(r):
    """
    Dada una fila de un archivo CSV extrae la información de un dependiente
    :param r: Fila de archivo CSV
    :return: Dependiente
    """
    dependiente = dict()
    dependiente['id'] = r[7]
    dependiente['1003'] = r[8]
    dependiente['1004'] = r[9]
    # dependiente['habeas_data'] = r[10]
    # dependiente['cedula_validada'] = r[11]
    dependiente['1005'] = r[12]
    dependiente['1006'] = r[13]
    dependiente['1007'] = r[14]
    dependiente['1008'] = r[15]
    dependiente['1009'] = r[16]
    dependiente['1010'] = r[17]
    dependiente['1012'] = r[18]
    dependiente['1013'] = r[19]
    dependiente['1014'] = r[20]
    dependiente['1016'] = r[21]
    # dependiente['hijos'] = r[22]
    # dependiente['parentezco_familiar'] = r[23]
    # dependiente['nombre_familiar'] = r[24]
    # dependiente['nacimiento_familiar'] = r[25]
    # dependiente['sexo_familiar'] = r[26]

    return dependiente


def cargar_arbol_a_tuplas(arbol, representantes, farmacias, dependientes):
    """
    Carga toda la información de la estructura generada por extract_tq_dependientes a tuplas para insertar a la tabla respuesta
from registro import utils
a,b,c,d = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ultra_simple.csv')
t = utils.cargar_arbol_a_tuplas(a,b,c,d)
    :param arbol: Arbol con los identificadores
    :param representantes: información de los representantes
    :param farmacias: Información de las farmacias
    :param dependientes: Información de los dependientes
    :return: Matriz con informacion insertada
    """
    tuplas_insertadas = []

    for id_representante, farmacias_representante in arbol.iteritems():
        for farmacia in farmacias_representante:
            id_farmacia = farmacia['id']
            dependientes_farmacia = farmacia['dependientes']
            tuplas_insertadas.append(
                (PREGUNTA_FARMACIA, id_farmacia, None, None)
            )
            for dependiente_farmacia in dependientes_farmacia:
                id_dependiente = dependiente_farmacia['id']
                tuplas_insertadas.append(
                    (PREGUNTA_DEPENDIENTE, id_dependiente, PREGUNTA_FARMACIA, id_farmacia)
                )
                index_dependiente = buscar_en_arreglo(id_dependiente, dependientes)
                if index_dependiente > -1:
                    dependiente = dependientes[index_dependiente]
                    dependientes.remove(dependiente)
                    print "Dependiente", dependiente['1004']
                    # print dependiente
                    dependiente.pop('id')
                    # print dependiente
                    for id_entrada, valor in dependiente.iteritems():
                        tuplas_insertadas.append(
                            (id_entrada, valor, PREGUNTA_DEPENDIENTE, id_dependiente)
                        )
                else:
                    print ("Esto no debería pasar, revisar el id_dependiente %s" % id_dependiente['id'])
    return tuplas_insertadas


def cargar_tuplas_a_bd(lista_tuplas):
    """
    Recibe una lista de tuplas y las inserta a la bd, cuyo primer elemento es el ID de entrada, el segundo el valor, el
    tercero el id de la entrada condicional y el 4 el valor de la entrada condicional
from registro import utils
a,b,c,d = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ultra_simple.csv')
t = utils.cargar_arbol_a_tuplas(a,b,c,d)
utils.cargar_tuplas_a_bd(t)
    :param lista_tuplas: Lista de tuplas
    :return: None
    """
    from . import models
    for id_entrada, valor, pregunta, valor_pregunta in lista_tuplas:
        entrada = models.Entrada.objects.get(pk=id_entrada)
        nueva_respuesta = models.Respuesta(
            valor=valor,
        )
        if pregunta is not None:
            nueva_respuesta.pregunta_id = int(pregunta)
            nueva_respuesta.respuesta = valor_pregunta
        nueva_respuesta.save()
        entrada.respuesta.add(nueva_respuesta)
        print nueva_respuesta


def eliminar_todas_respuestas():
    """
    Elimina todas las respuestas de la base de datos
    Usese con moderación
from registro import utils
utils.eliminar_todas_respuestas()
    :return: None
    """
    from . import models
    todas_las_respuestas = models.Respuesta.objects.all()
    for r in todas_las_respuestas:
        r.delete()

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