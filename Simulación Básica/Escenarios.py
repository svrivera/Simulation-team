
from Hospital import pacientes_del_dia

from random import seed

seed(2)



def generador(n_simulaciones, dias_totales):

    set_de_colas_por_replica = []
    for repica in range(n_simulaciones):
        colas_por_dia = []
        for dia in range(dias_totales):

            cola = pacientes_del_dia(dia)
            colas_por_dia.append(cola)

        set_de_colas_por_replica.append(colas_por_dia)

    return set_de_colas_por_replica


generador1 = lambda x, y, z, d: x * 0.6 + y + z if d else y
generador2 = lambda y, d: 0 if d else y
generador3 = lambda z, d: z * 0.4 if d else z