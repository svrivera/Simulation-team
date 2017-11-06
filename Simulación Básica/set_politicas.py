from Hospital import prioridad_grd

def politica_exquisita(self, n_llegadas, n_llegadas_totales, paciente, pacientes_externalizados_dia, camas_libres, r, i): #Cambiar nombre
    if len(camas_libres) * 1.3 <  n_llegadas - i and i < n_llegadas_totales * 0.6:
        recibir_priorizado_criticas(self, paciente, pacientes_externalizados_dia, camas_libres[0],r)
    else:
        recibir_todo_critica(self, paciente, camas_libres[0])
# Se activa cuando hay pocas camas
def recibir_priorizado_criticas(self, paciente, pacientes_externalizados_dia, cama, r):
    if paciente.ranking > r:
        cama.recibir_paciente(paciente)
    else:
        # No lo preferimos
        pacientes_externalizados_dia.append(paciente)








def recibir_todo_critica(self, paciente, cama):
    # Aumentamos en 1 el número de pacientes que llegan
    cama.recibir_paciente(paciente)



def recibir_todo_intermedia(self, paciente, pacientes_externalizados_dia):
    camas_libres = self.camas_intermedias_libres
    if len(camas_libres) > 0:
        # Si hay camas, tomo la primera
        cama = camas_libres[0]
        cama.recibir_paciente(paciente)
    else:
        # Si no hay camas libres, se externaliza
        pacientes_externalizados_dia.append(paciente)


def recibir_todo_basica(self, paciente, pacientes_externalizados_dia):
    camas_libres = self.camas_basicas_libres
    if len(camas_libres) > 0:
        # Si hay camas, tomo la primera
        cama = camas_libres[0]
        cama.recibir_paciente(paciente)
    else:
        # Si no hay camas libres, se externaliza
        pacientes_externalizados_dia.append(paciente)






politicas = {}