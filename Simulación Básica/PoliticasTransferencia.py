# Bajadas de Crítica a Intermedia:
#--------------------------------------------------------------------------------
#sin penalizacion
from Hospital import razon_deseada_intermedia


def bajar_minimo(self):
    camas_ordenadas = sorted(self.camas_criticas_ocupadas,
                             key=lambda x: x.dias_recomendados)

    for cama_origen in camas_ordenadas:
        if cama_origen.transferible:
            if cama_origen.siguiente_cama == "Intermedia":
                camas_libres = self.camas_intermedias_libres
            elif cama_origen.siguiente_cama == "Basica":
                camas_libres = self.camas_basicas_libres
            else:
                raise Exception("Cama solicitada no existe")

            if len(camas_libres) > 0:
                # Si hay camas, tomo la primera
                cama_destino = camas_libres[0]
                paciente = cama_origen.checkout()

                cama_destino.recibir_paciente(paciente)
            else:
                break

#--------------------------------------------------------------------------------

def bajar_todo_intermedia(self):
    # Intermedios
    camas_ordenadas = sorted(self.camas_intermedias_ocupadas,
                             key=lambda x: x.dias_recomendados)
    # Si quiero poner recomendado tambien hay que modificar la función transferible en la clase Cama para que vea el recomendado y no el minimo
    for cama_origen in camas_ordenadas:
        # Si ya cumplió con los días recomendados
        if cama_origen.transferible:
            camas_libres = self.camas_basicas_libres
            if len(camas_libres) > 0:
                # Si hay camas, tomo la primera
                cama_destino = camas_libres[0]
                paciente = cama_origen.checkout()
                cama_destino.recibir_paciente(paciente)
            else:
                # No hay camas libres en el nivel básico
                # Acá se debe agregar criterios de transferencia temprana de pacientes
                break


def bajar_solo_sin_penalizacion_intermedia(self):
    # Intermedios
    camas = self.camas_intermedias_sin_penalizacion
    # Si quiero poner recomendado tambien hay que modificar la función transferible en la clase Cama para que vea el recomendado y no el minimo
    for cama_origen in camas:
        camas_libres = self.camas_basicas_libres
        if len(camas_libres) > 0:
            # Si hay camas, tomo la primera
            cama_destino = camas_libres[0]
            paciente = cama_origen.checkout()
            cama_destino.recibir_paciente(paciente)
        else:
            # No hay camas libres en el nivel básico

            # Acá se debe agregar criterios de transferencia temprana de pacientes
            break


def bajar_critica_basica(self):
    # Intermedios
    camas = sorted(self.camas_criticas_a_basicas,
                             key=lambda x: x.paciente.dias_recomendados_i)
    # Si quiero poner recomendado tambien hay que modificar la función transferible en la clase Cama para que vea el recomendado y no el minimo
    for cama_origen in camas:
        camas_libres = self.camas_basicas_libres
        if len(camas_libres) > 0:
            # Si hay camas, tomo la primera
            cama_destino = camas_libres[0]
            paciente = cama_origen.checkout()
            cama_destino.recibir_paciente(paciente)
        else:
            # No hay camas libres en el nivel básico

            # Acá se debe agregar criterios de transferencia temprana de pacientes
            break

# BAJANDO DE CRITICA A INTERMEDIA

def bajar_todo_critica(self, *args):
    while len(self.camas_intermedias_libres) > 0 and len(self.camas_criticas_transferible) > 0:
        camas_libres = self.camas_intermedias_libres
        if len(self.camas_criticas_sin_penalizacion) > 0:
            cama_origen = self.camas_criticas_sin_penalizacion[0]
        else:
            cama_origen = sorted(self.camas_criticas_transferible, key=lambda cama: cama.dias_recomendados, reverse = True)[0]
        cama_destino = self.camas_intermedias_libres[0]
        paciente = cama_origen.checkout()

        cama_destino.recibir_paciente(paciente)


def bajar_con_reserva_moderada(self, llegadas_esperadas, sensibilidad):

    n_pedidas = len(self.camas_criticas_transferible)
    n_disponibles = len(self.camas_intermedias_libres)

    llegadas_esperadas_deseadas = int(llegadas_esperadas * razon_deseada_intermedia(self.ranking_promedio)) - sensibilidad

    razon_a_guardar = llegadas_esperadas_deseadas / (n_pedidas + llegadas_esperadas)
    n_reservadas = int(n_disponibles * razon_a_guardar)
    while (n_disponibles - n_reservadas) > 0 and len(self.camas_criticas_transferible) > 0:
        n_disponibles = len(self.camas_intermedias_libres)

        if len(self.camas_criticas_sin_penalizacion) > 0:
            cama_origen = self.camas_criticas_sin_penalizacion[0]
        else:
            cama_origen = sorted(self.camas_criticas_transferible, key=lambda cama: cama.dias_recomendados, reverse = True)[0]
        cama_destino = self.camas_intermedias_libres[0]
        paciente = cama_origen.checkout()

        cama_destino.recibir_paciente(paciente)


def bajar_con_reserva_agresiva(self, llegadas_esperadas, sensibilidad):

    n_pedidas = len(self.camas_criticas_transferible)
    n_disponibles = len(self.camas_intermedias_libres)

    llegadas_esperadas_deseadas = int(llegadas_esperadas * razon_deseada_intermedia(self.ranking_promedio)) + sensibilidad

    razon_a_guardar = llegadas_esperadas_deseadas / (n_pedidas + llegadas_esperadas)
    n_reservadas = int(n_disponibles * razon_a_guardar)

    print(n_reservadas)

    while (n_disponibles - n_reservadas) > 0 and len(self.camas_criticas_transferible) > 0:
        n_disponibles = len(self.camas_intermedias_libres)

        if len(self.camas_criticas_sin_penalizacion) > 0:
            cama_origen = self.camas_criticas_sin_penalizacion[0]
        else:
            cama_origen = sorted(self.camas_criticas_transferible, key=lambda cama: cama.dias_recomendados, reverse = True)[0]
        cama_destino = self.camas_intermedias_libres[0]
        paciente = cama_origen.checkout()

        cama_destino.recibir_paciente(paciente)

