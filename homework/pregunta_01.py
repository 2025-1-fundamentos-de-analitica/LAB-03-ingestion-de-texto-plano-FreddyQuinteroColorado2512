"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Quitar líneas vacías
    lines = [line.rstrip() for line in lines if line.strip()]

    # Detectar el índice de la primera línea de datos (empieza con número de cluster)
    start_index = 0
    for i, line in enumerate(lines):
        if re.match(r"\s*\d+\s+", line):  # Línea que comienza con un número
            start_index = i
            break

    content_lines = lines[start_index:]

    data = []
    current_row = None

    for line in content_lines:
        if re.match(r"\s*\d+\s+", line):
            # Es una nueva fila
            if current_row:
                data.append(current_row)

            parts = re.split(r"\s{2,}", line.strip(), maxsplit=3)
            cluster = int(parts[0])
            cantidad = int(parts[1])
            porcentaje = float(parts[2].replace(",", ".").replace("%", ""))
            palabras = parts[3].strip()
            current_row = [cluster, cantidad, porcentaje, palabras]
        else:
            # Línea de continuación de palabras clave
            if current_row:
                current_row[3] += " " + line.strip()

    # Agregar última fila
    if current_row:
        data.append(current_row)

    # Limpieza final de las palabras clave
    for row in data:
        palabras = row[3]
        palabras = re.sub(r"\s+", " ", palabras)
        palabras = re.sub(r"\.$", "", palabras)
        palabras = re.sub(r"\s*,\s*", ", ", palabras)
        row[3] = palabras.strip()

    # Crear DataFrame
    columns = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave"
    ]
    df = pd.DataFrame(data, columns=columns)
    return df