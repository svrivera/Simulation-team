from Politicas import Hospital as Sim1, deseados_criticos
from PoliticaAgresiva import Hospital as Sim2
#import numpy as np
#import pandas as pd
from Escenarios import generador1, generador2, generador3
from CargadorLlegadas import generador_llegadas
from collections import defaultdict
from random import seed
import pickle
from Estado import *

resp = ""
eleccion = {"1": Sim1, "2": Sim2}
while resp != "1" and resp != "2":
    resp = input("\n\nQué quieres hacer?:\n\n[1] Ver Anhealing\n[2] Ver Política Agresiva\n>\t")
Simulacion = eleccion[resp]

# Ingresamos los parámetros de la simulación
n_simulaciones = 30
tiempo_simulacion = 60
dia_transiente = 19

n_criticas=18
n_intermedias=31
n_basicas=213

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

d = True if resp == '2' else False

diferencia_min_recomendado_promedio = 0
# Paciente Bajados dias Minimos Critica
p_b_m_c = 0
p_b_r_c = 0
p_b_e_c = 0
p_b_directo_basica = 0
p_b_m_i = 0
p_b_r_i = 0
p_b_e_i = 0

set_colas = generador_llegadas(n_simulaciones, tiempo_simulacion + dia_transiente)
#with open("colas", "wb") as outfile:
#    pickle.dump(set_colas2, outfile)

p_llego_a_intermedia = 0

#set_colas2 = None

#with open("colas", "rb") as outfile:
#    set_colas = pickle.load(outfile)

interm = 0
print("\nSimulando... \n\n\n")
for i in range(n_simulaciones):
    Sim = Simulacion(tiempo_simulacion=tiempo_simulacion, dia_transiente=dia_transiente,
                   n_criticas=n_criticas,
                   n_intermedias=n_intermedias,
                   n_basicas=n_basicas,
                   cola_paciente = set_colas[i],
                   politica_hacia_intermedia = politicas_transferencia_hacia_intermedia,
                   politicas_llegadas_intermedias=politicas_llegadas_intermedias)
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

    interm += Sim.p_intermedios

    for lista in Sim.dados_alta_basica:
        for paciente in lista:
            dic_pacientes_atendidos[paciente.enfermedad] += 1

            if paciente.bajada_intermedia == 0:
                p_b_directo_basica += 1
            elif paciente.bajada_intermedia == 1:
                p_b_r_i += 1
            elif paciente.bajada_intermedia == 2:
                p_b_m_i += 1
            else:
                p_b_e_i += 1


            if paciente.bajada_critica == 1:
                p_b_r_c += 1
            elif paciente.bajada_critica == 2:
                p_b_m_c += 1
            elif paciente.bajada_critica == 3:
                p_b_e_c += 1
            else:
                p_llego_a_intermedia += 1

interm /= n_simulaciones




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

s += "Costo Externalización del Paciente (Promedio): {}\n\n".format(costo_global/derivados_global)

s += "Cantidad Promedio de Pacientes Derivados : {}\n\n".format(derivados_global/n_simulaciones)

x = generador2(p_b_e_c / n_simulaciones, d)
y = generador1(p_b_r_c / n_simulaciones, p_b_m_c / n_simulaciones, p_b_e_c / n_simulaciones, d)
z = generador3(p_b_r_c / n_simulaciones, d)

#s += "Diferencia con recomendado Promedio: {} \n\n".format(diferencia_min_recomendado_promedio/n_simulaciones)
s += "Número Promedio de Pacientes bajados directo desde Crítica a Básica: {}\n".format(p_b_directo_basica / n_simulaciones)
s += "Número Promedio de Pacientes bajados de Crítica con Tratamiento Completo: {}\n".format(z)
s += "Número Promedio de Pacientes bajados de Crítica con Tratamiento Mínimo: {}\n".format(y)

s += "\nNúmero Promedio de Pacientes Atendidos en Intermedia: {}\n\n".format(interm)

#s += "Número Promedio de Pacientes bajados de Crítica con Tratamiento Medio: {}\n".format(x)
#s += "Número Promedio de Pacientes bajados de Intermedia con Tratamiento Completo: {}\n".format(p_b_r_i / n_simulaciones)
#s += "Número Promedio de Pacientes bajados de Intermedia con Tratamiento Mínimo: {}\n".format(p_b_m_i / n_simulaciones)
#s += "Número Promedio de Pacientes bajados de Intermedia con Tratamiento Medio: {}\n\n".format(p_b_e_i / n_simulaciones)




#s += "Cantidad Promedio de Pacientes dados de Alta en cama Basica: {}\n".format(altas_basica/n_simulaciones)
#s += "Cantidad Promedio de Pacientes dados de Alta en cama Intermedia: {}\n".format(altas_intermedia/n_simulaciones)
#s += "Cantidad Promedio de Pacientes dados de Alta en cama Critica: {}\n".format(altas_criticas/n_simulaciones)
s += "Cantidad Promedio de Pacientes dados de Alta: {}\n\n".format(altas_global/n_simulaciones)

s += "Disponibilidad Camas Críticas: {:.2f}%\n".format(sum(disp_crit) / len(disp_crit))
s += "Disponibilidad Camas Intermedias: {:.2f}%\n".format(sum(disp_int) / len(disp_int))
s += "Disponibilidad Camas Básicas: {:.2f}%\n".format(sum(disp_bas) / len(disp_bas))
print(s)

print(dic_pacientes_atendidos)


def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


seguir = ""

while seguir != "0" and not d:
    seguir = input("\nIngrese una opción:\n[1] Consultar ingreso a Criticas\n"
                    "[2] Consultar ingreso a Intermedias\n"
                    "[3] Consultar transferencias a Intermedias\n"
                    "[0] Salir: \n>\t")
    if seguir == "1":
        n_camas_c_libres = "a"
        arribados = "a"
        n_traumatologico = "a"
        n_renal = "a"
        n_coronario = "a"
        n_respiratorio = "a"
        ranking = "a"

        while not n_camas_c_libres.isdigit():
            n_camas_c_libres = input("Número de camas Críticas disponibles: ")
        while not arribados.isdigit():
            arribados = input("Número de pacientes arribados en el día: ")
        while not n_traumatologico.isdigit():
            n_traumatologico = input("Número de pacientes Traumatológico arribados en el día: ")
        while not n_renal.isdigit():
            n_renal = input("Número de pacientes Renal arribados en el día: ")
        while not n_coronario.isdigit():
            n_coronario = input("Número de pacientes Coronario arribados en el día: ")
        while not n_respiratorio.isdigit():
            n_respiratorio = input("Número de pacientes Respiratorio arribados en el día: ")
        while not is_float(ranking):
            ranking = input("Ranking del sistema: ")

        deseados = deseados_criticos(float(ranking))
        aux = {"Traumatologico":n_traumatologico, "Renal":n_renal, "Coronario":n_coronario, "Respiratorio":n_respiratorio}

        estado = calcular_estado_recibir_critica(int(n_camas_c_libres) / n_criticas * 100, int(arribados), 5 * len(deseados),
                                                 sum(int(aux[x]) for x in deseados))
        boolean, txt = respuesta_gestor_recibir_c[estado]
        if boolean:
            print(txt.format(", ".join(deseados)))
        else:
            print(txt)

    elif seguir == "2":
        n_camas_i_libres = "a"
        arribados = "a"
        n_oftalmologicos = "a"
        n_esofagicos = "a"
        ranking = "a"
        while not n_camas_i_libres.isdigit():
            n_camas_i_libres = input("Número de camas Intermedias disponibles: ")
        while not arribados.isdigit():
            arribados = input("Número de pacientes arribados en el día: ")
        while not n_oftalmologicos.isdigit():
            n_oftalmologicos = input("Número de pacientes Oftalmológicos arribados en el día: ")
        while not n_esofagicos.isdigit():
            n_esofagicos = input("Número de pacientes Esofágicos arribados en el día: ")
        while not is_float(ranking):
            ranking = input("Ranking del sistema: ")
        estado = calcular_estado_recibir_intermedia(int(n_camas_i_libres)/n_intermedias*100, int(arribados), 10, int(n_esofagicos) + int(n_oftalmologicos))
        print(respuesta_gestor_recibir_i[estado])

    elif seguir == "3":
        n_camas_i_libres = "a"
        n_camas_c_libres = "a"
        transferibles = "a"
        ranking = "a"
        while not n_camas_i_libres.isdigit():
            n_camas_i_libres = input("Número de camas Intermedias disponibles: ")
        while not n_camas_c_libres.isdigit():
            n_camas_c_libres = input("Número de camas Críticas disponibles: ")
        while not transferibles.isdigit():
            transferibles = input("Número de pacientes transferibles en nivel Críticas: ")

        estado = calcular_estado_sistema_transferencia(int(n_camas_c_libres)/n_criticas * 100, int(n_camas_i_libres)/n_intermedias * 100)

        boolean, aux, txt = respuesta_gestor_transferencia[estado]

        if boolean:

            razon_a_guardar = 10 / (int(transferibles) + 10)

            n_bajar = min(int(n_camas_i_libres) - int(int(n_camas_i_libres) * razon_a_guardar + 2 * aux), int(transferibles))

            print(txt.format(n_bajar))
        else:
            if min(int(n_camas_i_libres), int(transferibles)) == int(transferibles):
                print("Bajar los {} pacientes críticos".format(int(transferibles)))
            else:
                print(txt.format(int(n_camas_i_libres)))






# ### # Buscamos el punto tranciente
# import matplotlib.pyplot as plt
# import pandas as pd
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
# lista1 = pd.DataFrame({'Datos':disponibilidad_dia_basica_promedio})
# lista2 = lista1.rolling(5).mean()
#
# plt.ylim([0,100])
# plt.plot(lista1)
# plt.plot(lista2)
# plt.ylabel('Disponibilidad camas')
# plt.xlabel('Días')
# plt.show()