import json
from datetime import date
from pathlib import Path
from docxtpl import DocxTemplate
""" from num2words import num2words """
from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from .models import Clientes, Inmueble


def serialize_date(obj):
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError("Type not serializable")


def index_contrato(req, id_inmueble):

    query = f"SELECT i.*, c.nom_cliente FROM inmueble i JOIN clientes c ON i.cliente_id = c.id_cliente WHERE i.id_inmueble = {id_inmueble}"

    ERR = ''
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            res = cursor.fetchall()

        # Convertir los resultados a una lista de diccionarios
        lista = []
        for row in res:
            row_dict = {}
            for i, value in enumerate(row):
                column_name = columns[i]
                row_dict[column_name] = value
            lista.append(row_dict)

        # Convertir a formato JSON
        res_JSON = json.dumps(lista, default=serialize_date)

    except IntegrityError as e:
        ERR = 'Algo fallo, intenta nuevamente o ponte en contacto con Admin'
        print("Error:", e)

    print(lista)
    context = {
        'inmuebles': lista,
        'error': ERR
    }

    return render(req, "contrato/contrato_form.html", context)


def crear_contrato(req):
    """ print(num2words(42))
    print(num2words(42, to='ordinal'))
    print(num2words(564267, lang='en')) """

    context = {
        """ "nom_propietario": propietario,
        "nom_cliente": cliente,
        "rg_cliente ": rg_cliente,
        "dni_cliente": dni_cliente,
        "dir_cliente": dir_cliente,
        "ciudad_cliente": ciudad_cliente,
        "tel_cliente": tel_cliente,
        "email_cliente": email_cliente,
        "nombre_inmueble": nombre_inmueble,
        "dir_inmueble": dir_inmueble,
        "ciudad_inmueble": ciudad_inmueble,
        "pass_hall1": pass_hall1,
        "pass_hall2": pass_hall2,
        "pass_wifi": pass_wifi,
        "num_apto": num_apto,
        "fecha_ing": fecha_ing,
        "fecha_salida": fecha_salida,
        "valor_inmueble": valor_inmueble,
        "valor_inmueble_palabras": valor_inmueble_palabras = num2words(valor_inmueble),
        "cant_dias": cant_dias,
        "valor_total": valor_total = (valor_inmueble * cant_dias) + 170,
        "valor_total_palabras": valor_total_palabras = num2words(valor_total),
        "monto_reserva": monto_reserva,
        "monto_reserva_palabras": monto_reserva_palabras = num2words(monto_reserva),
        "fecha_reserva": fecha_reserva,
        "datos_envio": datos_envio,
        "saldo_pendiente": saldo_pendiente = valor_total - monto_reserva,
        "habitac_maxima": habitac_maxima,
        "fecha_contrato": fecha_contrato, """
    }

    try:
        doc_Path = Path(__file__).parent  # ruta del proyecto
        doc_Arch = doc_Path / 'contrato_plantilla.docx'  # ruta del archivo DOCX Plantilla
        # ruta del archivo DOCX contrato completo Cliente
        doc = DocxTemplate(doc_Arch)
        doc.render(context)
        cliente = 'Fiamma'
        doc_Arch_completo = doc_Path / f'contrato_completo-{cliente}.docx'
        doc.save(doc_Arch_completo)
    except FileNotFoundError:
        print("El archivo no existe")
    except IsADirectoryError:
        print("El archivo es un directorio")
    except PermissionError:
        print("No tienes permisos para acceder al archivo")
    except Exception as e:
        print(f"Ocurrió un error: {e}")