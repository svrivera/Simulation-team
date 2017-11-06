
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

def bajar_todo_critica(self):
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


