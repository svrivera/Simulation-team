from .GRDS import *
from random import shuffle
from .Paciente import Paciente
from collections import deque
from numpy.random import poisson


def pacientes_del_dia(tiempo_actual):
    pacientes = []
    lista = [GRD_Coronario,
             GRD_Hepatico,
             GRD_Respiratorio,
             GRD_Renal,
             GRD_Neurologico,
             GRD_Traumatologico,
             GRD_Esofagico,
             GRD_Oftalmologico,
             GRD_Circulatorio,
             GRD_Intestinal]
    for grd in lista:
        for i in range(poisson(1)):
            pacientes.append(Paciente(tiempo_actual, grd))
    shuffle(pacientes)
    return deque(pacientes)