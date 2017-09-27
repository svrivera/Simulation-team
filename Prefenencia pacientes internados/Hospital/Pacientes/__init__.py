from .GRDS import *
from random import shuffle
from .Paciente import Paciente
from collections import deque
from numpy.random import poisson


# Creamos los pacientes que llegarán al hospital cada día
def pacientes_del_dia(tiempo_actual):
    pacientes = []
    lista_GRD = [GRD_Coronario,
             GRD_Hepatico,
             GRD_Respiratorio,
             GRD_Renal,
             GRD_Neurologico,
             GRD_Traumatologico,
             GRD_Esofagico,
             GRD_Oftalmologico,
             GRD_Circulatorio,
             GRD_Intestinal]

    for grd in lista_GRD:
        for i in range(poisson(grd.tasa_llegada)):
            pacientes.append(Paciente(tiempo_actual, grd))
    shuffle(pacientes)
    return deque(pacientes)
