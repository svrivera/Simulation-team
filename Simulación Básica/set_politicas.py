from Hospital import prioridad_grd

#  Llegadas:

#--------------------------------------------------------------------------------
# Se activa cuando hay pocas camas


def recibir_priorizado_criticas(self, paciente, cama, pacientes_externalizados_dia, r):
    if paciente.ranking > r:
        cama.recibir_paciente(paciente)
    else:
        # No lo preferimos
        pacientes_externalizados_dia.append(paciente)



def recibir_todo_critica(self, paciente, cama, *args):
    # Aumentamos en 1 el número de pacientes que llegan
    cama.recibir_paciente(paciente)

#--------------------------------------------------------------------------------


def recibir_todo_intermedia(self, paciente, cama, *args):
    # Si hay camas, tomo la primera
    cama.recibir_paciente(paciente)


def recibir_deseados_intermedia(self, paciente, cama, pacientes_externalizados_dia, deseados):
    if paciente.enfermedad in deseados:
        cama.recibir_paciente(paciente)
    else:
        pacientes_externalizados_dia.append(paciente)

#--------------------------------------------------------------------------------


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