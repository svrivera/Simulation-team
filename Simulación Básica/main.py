from Hospital import Simulacion


# Ingresamos los parámetros de la simulación
n_simulaciones = 100
tiempo_simulacion = 90

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

#Altas por cama
altas_intermedia = 0
altas_basica = 0
altas_criticas = 0

for i in range(n_simulaciones):
    s = Simulacion(tiempo_simulacion=tiempo_simulacion,
                   n_criticas=18,
                   n_intermedias=31,
                   n_basicas=213)

    s.run()

    costo_global += s.costo_externalizacion
    derivados_global += s.pacientes_derivados
    dias_extra_c += s.dias_extra_c
    dias_extra_i += s.dias_extra_i
    altas_intermedia += s.altas_dadas_intermedia
    altas_basica += s.altas_dadas_basica
    altas_criticas += s.altas_dadas_critica

    altas_global += s.altas_dadas_basica + s.altas_dadas_critica + s.altas_dadas_intermedia
    ####Para ver % ocupación
    disp_crit.append( sum(d[0] for d in s.disponibilidad) / len(s.disponibilidad))
    disp_int.append(sum(d[1] for d in s.disponibilidad) / len(s.disponibilidad))
    disp_bas.append(sum(d[2] for d in s.disponibilidad) / len(s.disponibilidad))



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





