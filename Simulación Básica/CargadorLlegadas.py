
from Hospital.Pacientes.GRDS import *
from Hospital.Pacientes import Paciente
from collections import deque
import json

NOMBRE_ARCHIVO = "colas.json"


GRDs = {}
GRDs["Coronario"] = GRD_Coronario
GRDs["Hepatico"] = GRD_Hepatico
GRDs["Respiratorio"] = GRD_Respiratorio
GRDs["Renal"] = GRD_Renal
GRDs["Neurologico"] = GRD_Neurologico
GRDs["Traumatologico"] = GRD_Traumatologico
GRDs["Esofagico"] = GRD_Esofagico
GRDs["Oftalmologico"] = GRD_Oftalmologico
GRDs["Circulatorio"] = GRD_Circulatorio
GRDs["Intestinal"] = GRD_Intestinal


with open(NOMBRE_ARCHIVO, "r") as outfile:
    set_colas = json.load(outfile)

def generar_dia(cola_con_nombres, tiempo_actual):
    llegadas_dia = []

    for grd in cola_con_nombres:
        llegadas_dia.append(Paciente(tiempo_actual, GRDs[grd]))

    return deque(llegadas_dia)


def generador_llegadas(n_simulaciones, dias_totales):

    set_de_colas_por_replica = []
    for replica in range(n_simulaciones):
        colas_por_dia = []
        for dia in range(dias_totales):

            cola = generar_dia(set_colas[replica][dia], dia)
            colas_por_dia.append(cola)

        set_de_colas_por_replica.append(colas_por_dia)

    return set_de_colas_por_replica