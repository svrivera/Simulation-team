from Politicas import Hospital as Simulacion
import numpy as np
import pandas as pd
from Escenarios import generador
from collections import defaultdict
from random import seed


seed(4)
# Ingresamos los parámetros de la simulación
n_simulaciones = 30
tiempo_simulacion = 60
dia_transiente = 29

# Inicializamos los contadores que serán las métricas
costo_global = 0
derivados_global = 0
altas_global = 0
dias_extra_c = 0
dias_extra_i = 0

# Disponibilidades
disp_crit = []
disp_int = []
disp_bas = []

# Altas por cama
altas_intermedia = 0
altas_basica = 0
altas_criticas = 0

#
disponibilidad_por_dia_critica = []
disponibilidad_por_dia_intermedia = []
disponibilidad_por_dia_basica = []

#
set_colas = generador(n_simulaciones, tiempo_simulacion)


for i in range(n_simulaciones):
    Sim = Simulacion(tiempo_simulacion=tiempo_simulacion, dia_transiente=dia_transiente,
                   n_criticas=18,
                   n_intermedias=31,
                   n_basicas=213,
                   cola_paciente = set_colas[i])
    Sim.preparacion()

    Sim.run()

    costo_global += Sim.costo_externalizacion
    derivados_global += Sim.pacientes_derivados
    dias_extra_c += Sim.dias_extra_c
    dias_extra_i += Sim.dias_extra_i
    altas_intermedia += Sim.altas_dadas_intermedia
    altas_basica += Sim.altas_dadas_basica
    altas_criticas += Sim.altas_dadas_critica

    altas_global += Sim.altas_dadas_basica + Sim.altas_dadas_critica + Sim.altas_dadas_intermedia
    ####Para ver % ocupación
    disp_crit.append(sum(d[0] for d in Sim.disponibilidad) / len(Sim.disponibilidad))
    disp_int.append( sum(d[1] for d in Sim.disponibilidad) / len(Sim.disponibilidad))
    disp_bas.append( sum(d[2] for d in Sim.disponibilidad) / len(Sim.disponibilidad))

    disponibilidad_por_dia_critica.append([d[0] for d in Sim.disponibilidad])
    disponibilidad_por_dia_intermedia.append([d[1] for d in Sim.disponibilidad])
    disponibilidad_por_dia_basica.append([d[2] for d in Sim.disponibilidad])

    dic_pacientes_atendidos = defaultdict(int)

    for lista in Sim.dados_alta_basica:
        for paciente in lista:
            dic_pacientes_atendidos[paciente.enfermedad] += 1



disponibilidad_dia_critica_promedio = []
disponibilidad_dia_intermedia_promedio = []
disponibilidad_dia_basica_promedio = []


for dia in range(tiempo_simulacion):
    disponibilidad_dia_critica_promedio.append(sum(x[dia] for x in disponibilidad_por_dia_critica)/n_simulaciones)
    disponibilidad_dia_intermedia_promedio.append(sum(x[dia] for x in disponibilidad_por_dia_intermedia)/n_simulaciones)
    disponibilidad_dia_basica_promedio.append(sum(x[dia] for x in disponibilidad_por_dia_basica)/n_simulaciones)





s = ""
s += "Número de Simulaciones: {}\n".format(n_simulaciones)
s += "Días Simulados: {}\n\n".format(tiempo_simulacion)

s += "Costo Externalización Promedio: {}\n\n".format(costo_global/n_simulaciones)

s += "Cantidad Promedio de Pacientes Derivados : {}\n\n".format(derivados_global/n_simulaciones)

s += "Cantidad Promedio de Pacientes dados de Alta en cama Basica: {}\n".format(altas_basica/n_simulaciones)
s += "Cantidad Promedio de Pacientes dados de Alta en cama Intermedia: {}\n".format(altas_intermedia/n_simulaciones)
s += "Cantidad Promedio de Pacientes dados de Alta en cama Critica: {}\n".format(altas_criticas/n_simulaciones)
s += "Cantidad Promedio de Pacientes dados de Alta: {}\n\n".format(altas_global/n_simulaciones)

s += "Días Promedio Perdidos en Críticas: {}\n".format(dias_extra_c/n_simulaciones)
s += "Días Promedio Perdidos en Intermedias: {}\n".format(dias_extra_i/n_simulaciones)


s += "Disponibilidad Camas Críticas: {:.2f}%\n".format(sum(disp_crit) / len(disp_crit))
s += "Disponibilidad Camas Intermedias: {:.2f}%\n".format(sum(disp_int) / len(disp_int))
s += "Disponibilidad Camas Básicas: {:.2f}%\n".format(sum(disp_bas) / len(disp_bas))
print(s)

print(dic_pacientes_atendidos)


# # Buscamos el punto transciente
#
#
# # Guardamos en excel
# with open("DisponibilidadCriticas.csv", "w") as outfile:
#     outfile.write("Día;Disponibilidad\n")
#     for i, dato in enumerate(disponibilidad_dia_critica_promedio):
#         outfile.write(str(i+1)+";"+str(dato).replace(".", ",")+"\n")
#
# with open("DisponibilidadIntermedias.csv", "w") as outfile:
#     outfile.write("Día;Disponibilidad\n")
#     for i, dato in enumerate(disponibilidad_dia_intermedia_promedio):
#         outfile.write(str(i+1)+";"+str(dato).replace(".", ",")+"\n")
#
# with open("DisponibilidadBasica.csv", "w") as outfile:
#     outfile.write("Día;Disponibilidad\n")
#     for i, dato in enumerate(disponibilidad_dia_basica_promedio):
#         outfile.write(str(i+1)+";"+str(dato).replace(".", ",")+"\n")
#
#
# #Asi se usa
# lista1 = pd.DataFrame({'Datos':disponibilidad_dia_basica_promedio})
# lista2 = lista1.rolling(5).mean()
#
#
# import matplotlib.pyplot as plt
# plt.plot(lista1)
# plt.plot(lista2)
# plt.ylabel('Disponibilidad camas')
# plt.xlabel('Días')
# plt.show()