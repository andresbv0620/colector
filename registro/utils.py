#! -*- coding: utf-8 -*-
import csv
import codecs
from django.core import serializers
# =============== Funciones para leer CSV formato UTF - 8 ===============

PREGUNTA_FARMACIA = 997
PREGUNTA_DEPENDIENTE = 998
PREGUNTA_CEDULA = 1004


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


def merge_columns(path, output_path, column1, column2):
    """
    Toma un archivo csv y junta las columnas column1 y column2
from registro import utils
# utils.merge_columns('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/nuevo_dep.csv', "/Users/ma0/Desktop/contraslash/projects/colector_project/colector/nuevo_dep1.csv", 2, 4)
# utils.merge_columns('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/nuevo_dep1.csv', "/Users/ma0/Desktop/contraslash/projects/colector_project/colector/nuevo_dep2.csv", 9, 7)
# utils.merge_columns('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/nuevo_dep2.csv', "/Users/ma0/Desktop/contraslash/projects/colector_project/colector/nuevo_dep3.csv", 12, 7)
utils.merge_columns('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/nuevo_dep3.csv', "/Users/ma0/Desktop/contraslash/projects/colector_project/colector/nuevo_dep4.csv", 13, 7)
    :param path: Ruta del archivo
    :param output_path: Ruta destino del archivo
    :param column1: Columna para juntar
    :param column2: Columna para juntar
    :return:
    """
    archivo = codecs.open(path, 'r', encoding="utf-8", errors='ignore')
    salida = codecs.open(output_path, 'w+', encoding="utf-8")
    lineas = archivo.readlines()
    reader = unicode_csv_reader(lineas)

    for r in reader:
        for i in range(len(r)):
            a = ""
            if i == column2:
                a = "\"%s %s\"," % (r[i], r[column1])
            else:
                a = "\"%s\"," % (r[i])
            salida.write(a)
        salida.write("\n")
    salida.close()


# ============== Extraer dependientes de TQ ===================


def extract_tq_dependientes(path):
    """
    Dado un archivo proveido por tecnoquímicas, extraer la información necesaria estructurada en un arbol de dependencias
    Para usar desde consola.
    Uso:
from registro import utils
a,b,c,d, e = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ultra_simple_ajustado.csv')
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
    ids_beneficiarios = []
    beneficiarios = []

    arbol = dict()
    for r in reader:
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
            beneficiarios.append(extraer_beneficiarios(r))
            arbol[r[2]][ubicacion_farmacia]['dependientes'].append({'id': r[7]})
        # print arbol

    return (
        arbol,
        representantes,
        farmacias,
        dependientes,
        beneficiarios
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
    # Id Dependiente
    dependiente['id'] = r[7]
    # Tipo Documento
    dependiente['1003'] = r[8]
    # Identificacion
    dependiente['1004'] = r[9]
    # dependiente['habeas_data'] = r[10]
    # dependiente['cedula_validada'] = r[11]
    # Nombres
    dependiente['1005'] = r[12]
    # Apellidos
    dependiente['1006'] = r[13]
    # Fecha de Nacimiento
    dependiente['1007'] = r[14]
    # Genero
    dependiente['1008'] = r[15]
    # Estado Civil
    dependiente['1009'] = r[16]
    # Correo electrónico
    dependiente['1010'] = r[17]
    # Deportes
    dependiente['1026'] = r[18]
    # Hobby Personal
    dependiente['1027'] = r[19]
    # Hobby Familiar
    dependiente['1028'] = r[20]
    # Nivel de Escolaridad
    dependiente['1025'] = r[21]
    # Telefono Fijo
    dependiente['1012'] = r[22]
    # Telefono Celular
    dependiente['1013'] = r[23]
    # Direccion
    dependiente['1014'] = r[24]
    # Numero de Hijos
    dependiente['1029'] = r[25]
    # Titulo Profesional
    dependiente['1016'] = r[26]
    # Servicios Adicionales
    dependiente['1032'] = r[27]
    # dependiente['hijos'] = r[22]
    # dependiente['parentezco_familiar'] = r[23]
    # dependiente['nombre_familiar'] = r[24]
    # dependiente['nacimiento_familiar'] = r[25]
    # dependiente['sexo_familiar'] = r[26]

    return dependiente


def extraer_beneficiarios(r):
    """
    Dada una fila de un archivo CSV extrae la información de los beneficiarios
    :param r: Fila de archivo CSv
    :return: beneficiarios
    """
    beneficiario = dict()
    beneficiario['id'] = r[7]
    beneficiario['beneficiarios'] = []
    parentescos = r[28].split(",")
    nombres = r[29].split(",")
    nacimientos = r[30].split(",")
    sexos = r[31].split(",")
    max_items = max(
        len(parentescos),
        len(nombres),
        len(nacimientos),
        len(sexos),
    )
    for i in range(max_items):
        parentesco = ""
        nombre = ""
        nacimiento = ""
        sexo = ""
        try:
            parentesco = parentescos[i]
        except IndexError as ie:
            pass
        try:
            nombre = nombres[i]
        except IndexError as ie:
            pass
        try:
            nacimiento = nacimientos[i]
        except IndexError as ie:
            pass
        try:
            sexo = sexos[i]
        except IndexError as ie:
            pass
        b = dict()
        b['1020'] = parentesco
        b['1021'] = nombre
        b['1022'] = nacimiento
        b['1023'] = sexo
        beneficiario['beneficiarios'].append(b)
    return beneficiario


def cargar_arbol_a_tuplas(arbol, representantes, farmacias, dependientes, beneficiarios):
    """
    Carga toda la información de la estructura generada por extract_tq_dependientes a tuplas para insertar a la tabla respuesta
from registro import utils
a,b,c,d,e  = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ultra_simple.csv')
t = utils.cargar_arbol_a_tuplas(a,b,c,d,e)

# Solo para testing
from registro import utils
# Eliminamos las respuestas
utils.eliminar_todas_respuestas()
# Cargamos las respuestas del formulario
utils.guardar_archivo_serializado_base_de_datos('data.json')
# Cargamos la data al formulario
a,b,c,d,e  = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ultra_simple.csv')
t = utils.cargar_arbol_a_tuplas(a,b,c,d,e)
utils.cargar_tuplas_a_bd(t)

# Verificar departamento y ciudad
from pprint import pprint
from registro import utils
a,b,c,d,e  = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ultra_simple_ajustado.csv')
t = utils.cargar_arbol_a_tuplas(a,b,c,d,e)
pprint(t)
    :param arbol: Arbol con los identificadores
    :param representantes: información de los representantes
    :param farmacias: Información de las farmacias
    :param dependientes: Información de los dependientes
    :param beneificiarios: Información de los beneficiarios
    :return: Matriz con informacion insertada
    """
    tuplas_insertadas = []

    for id_representante, farmacias_representante in arbol.iteritems():
        print ("Id Representante", id_representante)
        for farmacia in farmacias_representante:
            id_farmacia = farmacia['id']
            dependientes_farmacia = farmacia['dependientes']
            tuplas_insertadas.append(
                (PREGUNTA_FARMACIA, id_farmacia, None, None, id_representante)
            )
            index_farmacia = buscar_en_arreglo(id_farmacia, farmacias)
            if index_farmacia > -1:
                farmacia = farmacias[index_farmacia]
                farmacias.remove(farmacia)
                farmacia.pop('id')
                for id_entrada, valor in farmacia.iteritems():
                    tuplas_insertadas.append(
                        (id_entrada, valor, PREGUNTA_FARMACIA, id_farmacia, id_representante)
                    )
            for dependiente_farmacia in dependientes_farmacia:
                id_dependiente = dependiente_farmacia['id']
                tuplas_insertadas.append(
                    (PREGUNTA_DEPENDIENTE, id_dependiente, PREGUNTA_FARMACIA, id_farmacia, id_representante)
                )
                index_dependiente = buscar_en_arreglo(id_dependiente, dependientes)
                if index_dependiente > -1:
                    # Adding dependientes
                    dependiente = dependientes[index_dependiente]
                    dependientes.remove(dependiente)
                    # print dependiente
                    dependiente.pop('id')
                    # print dependiente
                    for id_entrada, valor in dependiente.iteritems():
                        tuplas_insertadas.append(
                            (id_entrada, valor, PREGUNTA_DEPENDIENTE, id_dependiente, id_representante)
                        )

                    # Adding beneficiarios
                    beneficiario = beneficiarios[index_dependiente]
                    beneficiarios.remove(beneficiario)
                    for b in beneficiario['beneficiarios']:
                        for id_entrada, valor in b.iteritems():
                            tuplas_insertadas.append(
                                (id_entrada, valor, PREGUNTA_DEPENDIENTE, id_dependiente, id_representante)
                            )
                else:
                    print ("Esto no debería pasar, revisar el id_dependiente %s" % id_dependiente['id'])
    return tuplas_insertadas


def cargar_tuplas_a_bd(lista_tuplas):
    """
    Recibe una lista de tuplas y las inserta a la bd, cuyo primer elemento es el ID de entrada, el segundo el valor, el
    tercero el id de la entrada condicional y el 4 el valor de la entrada condicional
from registro import utils
a,b,c,d,e = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ultra_simple_ajustado.csv')
t = utils.cargar_arbol_a_tuplas(a,b,c,d,e)
utils.cargar_tuplas_a_bd(t)


# Prueba con archivo completo
from registro import utils
# Eliminamos las respuestas
utils.eliminar_todas_respuestas()
# Cargamos las respuestas del formulario
utils.guardar_archivo_serializado_base_de_datos('data.json')
# Cargamos la data al formulario
from registro import utils
utils.eliminar_respuestas_formulario(229)
a,b,c,d,e = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ultra_simple.csv')
t = utils.cargar_arbol_a_tuplas(a,b,c,d,e)
utils.cargar_tuplas_a_bd(t)
# Corregir el problema de beneficiarios
from registro import utils
utils.eliminar_respuestas_formulario(229)
a,b,c,d,e = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ajustado_corregido_minimo.csv')
t = utils.cargar_arbol_a_tuplas(a,b,c,d,e)
# from pprint import pprint
# pprint(t)
utils.cargar_tuplas_a_bd(t)
    :param lista_tuplas: Lista de tuplas
    :return: None
    """
    from . import models
    for id_entrada, valor, pregunta, valor_pregunta, id_representante in lista_tuplas:
        entrada = models.Entrada.objects.get(pk=id_entrada)
        nueva_respuesta = models.Respuesta(
            valor=valor,
            usuario=obtener_usuario_de_id_representante(id_representante)
        )
        if pregunta is not None:
            nueva_respuesta.pregunta_id = int(pregunta)
            nueva_respuesta.respuesta = valor_pregunta
        nueva_respuesta.save()
        entrada.respuesta.add(nueva_respuesta)


def generar_archivo_sql(lista_tuplas, archivo):
    """
    Genera un archivo sql de nombre archivo para agilizar el proceso de subida de datos
from registro import utils
a,b,c,d,e = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_definitivo.csv')
t = utils.cargar_arbol_a_tuplas(a,b,c,d,e)
utils.generar_archivo_sql(t, 'tq_dependientes_5.sql')
    :param lista_tuplas: lista de tuplas
    :param archivo nombre del archivo
    :return:
    """
    archivo = codecs.open(archivo, 'w+', encoding="UTF-8")
    from . import models
    for id_entrada, valor, pregunta, valor_pregunta, id_representante in lista_tuplas:
        entrada = models.Entrada.objects.get(pk=id_entrada)
        nueva_respuesta = models.Respuesta(
            valor=valor,
        )
        pregunta_id = 0
        respuesta = ""
        usuario=obtener_usuario_de_id_representante(id_representante).id

        if pregunta is not None:
            pregunta_id = int(pregunta)
            respuesta = valor_pregunta
        else:
            pregunta_id = "NULL"
            respuesta = ""
        archivo.write(
            "WITH X AS (INSERT INTO registro_respuesta (valor, pregunta_id, respuesta, usuario_id) VALUES ('%s',%s,'%s',%s) RETURNING id)\n" % (
                nueva_respuesta.valor,
                pregunta_id,
                respuesta,
                usuario
            )
        )
        archivo.write(
            "INSERT INTO registro_entrada_respuesta (entrada_id, respuesta_id) SELECT %d, id from X;\n" % entrada.id
        )
    archivo.close()


def obtener_usuario_de_id_representante(id_representante):
    """
    Obtiene un usuario dado un id de representante
    :param id_representante: id del representante
    :return:
    """
    from django.contrib.auth.models import User
    # Leer un archivo es muy pesado, así que se carga en memoria
    a = dict()
    a['10870'] = 577
    a['14722'] = 578
    a['6143'] = 579
    a['7041'] = 580
    a['6223'] = 581
    a['10706'] = 582
    a['10861'] = 583
    a['10862'] = 584
    a['10869'] = 585
    a['10863'] = 586
    a['9375'] = 587
    a['5643'] = 588
    a['5902'] = 589
    a['8976'] = 590
    a['8946'] = 591
    a['11191'] = 592
    a['12886'] = 593
    a['11602'] = 594
    a['14290'] = 595
    a['12909'] = 596
    a['11520'] = 597
    a['13433'] = 598
    a['2161'] = 599
    a['7165'] = 600
    a['14007'] = 601
    a['13757'] = 602
    a['4407'] = 603
    a['14291'] = 604
    return User.objects.get(pk=a[id_representante])


def cargar_arbol_a_diccionario(arbol, representantes, farmacias, dependientes, beneficiarios):
    """
    Carga toda la información de la estructura generada por extract_tq_dependientes a documento json para insertar a mongo
from registro import utils
a,b,c,d,e  = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ajustado_corregido_minimo.csv')
t = utils.cargar_arbol_a_diccionario(a,b,c,d,e)
from pprint import pprint
pprint(t)
    :param arbol: Arbol con los identificadores
    :param representantes: información de los representantes
    :param farmacias: Información de las farmacias
    :param dependientes: Información de los dependientes
    :param beneificiarios: Información de los beneficiarios
    :return: Matriz con informacion insertada
    """
    documentos_insertados = []

    for id_representante, farmacias_representante in arbol.iteritems():
        print ("Id Representante", id_representante)
        for farmacia in farmacias_representante:
            id_farmacia = farmacia['id']
            dependientes_farmacia = farmacia['dependientes']
            # tuplas_insertadas.append(
            #     (PREGUNTA_FARMACIA, id_farmacia, None, None, id_representante)
            # )
            index_farmacia = buscar_en_arreglo(id_farmacia, farmacias)
            if index_farmacia > -1:
                farmacia = farmacias[index_farmacia]
                farmacias.remove(farmacia)
                farmacia.pop('id')
                # for id_entrada, valor in farmacia.iteritems():
                #     tuplas_insertadas.append(
                #         (id_entrada, valor, PREGUNTA_FARMACIA, id_farmacia, id_representante)
                #     )
            documento = dict()
            documento['colector_id'] = obtener_usuario_de_id_representante(id_representante).id
            for dependiente_farmacia in dependientes_farmacia:
                id_dependiente = dependiente_farmacia['id']
                # tuplas_insertadas.append(
                #     (PREGUNTA_DEPENDIENTE, id_dependiente, PREGUNTA_FARMACIA, id_farmacia, id_representante)
                # )
                index_dependiente = buscar_en_arreglo(id_dependiente, dependientes)
                if index_dependiente > -1:
                    # Adding dependientes
                    dependiente = dependientes[index_dependiente]
                    dependientes.remove(dependiente)
                    # print dependiente
                    dependiente.pop('id')
                    # print dependiente
                    responses = transformar_dicionario_a_json(dependiente)
                    # Agregamos valores comunes
                    responses += [
                        {'input_id': PREGUNTA_FARMACIA, 'value': id_farmacia},
                        {'input_id': PREGUNTA_DEPENDIENTE, 'value': id_dependiente},
                    ]

                    documento['responses']  = responses

                    # Adding beneficiarios
                    # beneficiario = beneficiarios[index_dependiente]
                    # beneficiarios.remove(beneficiario)
                    # for b in beneficiario['beneficiarios']:
                    #     for id_entrada, valor in b.iteritems():
                    #         tuplas_insertadas.append(
                    #             (id_entrada, valor, PREGUNTA_DEPENDIENTE, id_dependiente, id_representante)
                    #         )
                else:
                    print ("Esto no debería pasar, revisar el id_dependiente %s" % id_dependiente['id'])
                documentos_insertados.append(documento)
    return documentos_insertados


def cargar_documentos_a_mongo(documentos):
    """
    Carga una lista de documentos a MongoDB
from registro import utils
a,b,c,d,e  = utils.extract_tq_dependientes('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_ajustado_corregido_minimo.csv')
t = utils.cargar_arbol_a_diccionario(a,b,c,d,e)
utils.cargar_documentos_a_mongo(t)
    :param documentos: Lista de docmentos
    :return: None
    """
    import pymongo
    from pymongo.errors import BulkWriteError
    servidor = pymongo.MongoClient('localhost', 27017)
    database = servidor.colector
    try:
        database.filled_forms.insert_many(documentos)
    except BulkWriteError as bwe:
        print(bwe.details)
    # for data in documentos:
    #     database.filled_forms.insert(data)


def transformar_dicionario_a_json(diccionario):
    """
    Transforma un diccionario a un documento json
    :param diccionario: diccionario python
    :return: documento string json
    """
    import json
    documento_json = ""
    respuestas = []
    for id_entrada, valor in diccionario.iteritems():
        d = dict()
        d['input_id'] = id_entrada
        d['value'] = valor
        respuestas.append(d)
    # documento_json = json.dumps(diccionario)
    # return documento_json
    return respuestas


def extraer_cedulas_no_validadas(path):
    """
    Recibe un archivo CSV de TQ y extrae una lista de las cedulas que deben ser validadas
from registro import utils
e = utils.extraer_cedulas_no_validadas('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_definitivo.csv')

    :param path:
    :return:
    """
    archivo = codecs.open(path, 'r', encoding="utf-8", errors='ignore')
    lineas = archivo.readlines()
    reader = unicode_csv_reader(lineas)
    line = 0
    cedulas_no_validadadas = set()

    for r in reader:
        line += 1
        if line < 3:
            continue

        if r[11] == "0":
            cedulas_no_validadadas.add(r[9])
    return cedulas_no_validadadas


def cambiar_texto_cedulas_no_validadas(cedulas_no_validadas):
    """
    Cambia el valor de una cédula
from registro import utils
e = utils.extraer_cedulas_no_validadas('/Users/ma0/Desktop/contraslash/projects/colector_project/colector/dependientes_definitivo.csv')

# Produccion
from registro import utils
e = utils.extraer_cedulas_no_validadas('/home/ubuntu/colector/dependientes_definitivo.csv')
utils.cambiar_texto_cedulas_no_validadas(e)
    :param cedulas_no_validadas:
    :return:
    """
    from registro import models
    pregunta_cedula = models.Entrada.objects.get(pk=PREGUNTA_CEDULA)
    todas_las_respuestas = pregunta_cedula.respuesta
    for c in cedulas_no_validadas:
        respuestas = todas_las_respuestas.filter(
            valor=c
        )
        for r in respuestas:
            r.valor = "%s (verificar)" % r.valor
            r.save()
        # if len(respuestas) > 1:
        #     print (len(respuestas), respuestas)


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


def eliminar_respuestas_formulario(id_formulario):
    """
    Elimina todas las respuestas relacionadas con un formulario de la base de datos
    Usese con moderación
from registro import utils
utils.eliminar_respuestas_formulario(229)
    :param id_formulario: Id del formulario
    :return:
    """
    from . import models
    try:
        formulario = models.Formulario.objects.get(pk=id_formulario)
        fichas = formulario.ficha.all()
        entradas_ids = []
        for ficha in fichas:
            entradas_ids.extend([x.id for x in ficha.entrada.all()])
        entradas = models.Entrada.objects.filter(id__in=entradas_ids)
        respuestas_ids = []
        for entrada in entradas:
            respuestas_ids.extend([x.id for x in entrada.respuesta.all()])
        respuestas = models.Respuesta.objects.filter(id__in=respuestas_ids)
        for r in respuestas:
            r.delete()
    except models.Formulario.DoesNotExist:
        print ("El formulario no existe")


def eliminar_respuestas_entrada(id_entrada):
    """
    Elimina todas las respuestas relacionadas a una entrada
from registro import utils
utils.eliminar_respuestas_entrada(1020)
utils.eliminar_respuestas_entrada(1021)
utils.eliminar_respuestas_entrada(1022)
utils.eliminar_respuestas_entrada(1023)
    :param id_entrada:
    :return:
    """
    from . import models
    try:
        entrada = models.Entrada.objects.get(pk=id_entrada)
        respuestas_ids = [x.id for x in entrada.respuesta.all()]
        respuestas = models.Respuesta.objects.filter(id__in=respuestas_ids)
        print (len(respuestas))
        for r in respuestas:
            r.delete()
    except models.Formulario.DoesNotExist:
        print ("El formulario no existe")
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