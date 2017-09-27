from Hospital import Simulacion


# Ingresamos los parámetros de la simulación
n_simulaciones = 1000
tiempo_simulacion = 30

# Inicializamos los contadores que serán las métricas
costo_global = 0
derivados_global = 0
altas_global = 0
dias_extra_c = 0
dias_extra_i = 0

for i in range(n_simulaciones):
    s = Simulacion(tiempo_simulacion=tiempo_simulacion,
                   n_criticas=18,
                   n_intermedias=31,
                   n_basicas=213)

    s.run()

    costo_global += s.costo_externalizacion
    derivados_global += s.pacientes_derivados
    altas_global += s.altas_dadas
    dias_extra_c += s.dias_extra_c
    dias_extra_i += s.dias_extra_i

s = ""
s += "Número de Simulaciones: {}\n".format(n_simulaciones)
s += "Días Simulados: {}\n\n".format(tiempo_simulacion)

s += "Costo Externalización Promedio: {}\n\n".format(costo_global/n_simulaciones)

s += "Cantidad Promedio de Pacientes Derivados : {}\n".format(derivados_global/n_simulaciones)
s += "Cantidad Promedio de Pacientes dados de Alta: {}\n\n".format(altas_global/n_simulaciones)

s += "Días Promedio Perdidos en Críticas: {}\n".format(dias_extra_c/n_simulaciones)
s += "Días Promedio Perdidos en Intermedias: {}\n".format(dias_extra_i/n_simulaciones)

print(s)




