from .GRDS import *
from random import shuffle
from .Paciente import Paciente
from collections import deque
from numpy.random import poisson

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
# Creamos los pacientes que llegarán al hospital cada día
def pacientes_del_dia(tiempo_actual):
    pacientes = []


    for grd in lista_GRD:
        for i in range(poisson(grd.tasa_llegada)):
            pacientes.append(Paciente(tiempo_actual, grd))


    shuffle(pacientes)
    return deque(pacientes)

llegadas_esperadas_criticas = sum(map(lambda grd: int(grd.tasa_llegada), filter(lambda grd: grd.tiempo_minimo[0] > 0, lista_GRD)))
llegadas_esperadas_intermedias = sum(map(lambda grd: int(grd.tasa_llegada), filter(lambda grd: grd.tiempo_minimo[0] <= 0, lista_GRD)))

def razon_deseada_intermedia(promedio):
    denominador = sum(map(lambda grd: int(grd.tasa_llegada),
                          filter(lambda grd: grd.tiempo_minimo[0] <= 0, lista_GRD)
                          ))
    numerador = sum(map(lambda grd: int(grd.tasa_llegada),
                        filter(lambda grd: grd.tiempo_minimo[0] <= 0 and grd.ranking > promedio, lista_GRD)
                        ))
    return numerador / denominador

def deseados_criticos(promedio):
    return list(map(lambda grd: grd.nombre, filter(lambda x: x.ranking > promedio, filter(lambda grd: grd.tiempo_minimo[0] > 0, lista_GRD))))

def deseados_intermedias(promedio):
    return list(map(lambda grd: grd.nombre, filter(lambda x: x.ranking > promedio, filter(lambda grd: grd.tiempo_minimo[0] <= 0, lista_GRD))))

if __name__ == '__main__':
    print(llegadas_esperadas_criticas)
    print(llegadas_esperadas_intermedias)