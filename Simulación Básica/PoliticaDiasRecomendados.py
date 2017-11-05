from Hospital import HospitalBase, CamaIntermedia, CamaCritica, CamaBasica, pacientes_del_dia
from time import time


class Hospital(HospitalBase):


    def __init__(self, tiempo_simulacion, n_criticas, n_intermedias, n_basicas):
        super().__init__(tiempo_simulacion, n_criticas, n_intermedias, n_basicas)



    # ----------------------------------------------------------------------------

    def run(self):
        tiempo_inicio = time()

        while self.tiempo_actual < self.tiempo_simulacion:

            # -------------------------------------------------------------------
            # Setup Inicial del dia
            pacientes_externalizados_dia = []
            dados_alta_critica = []
            dados_alta_intermedia = []
            dados_alta_basica = []
            # ------------------------------------------------------------------
            # Dar de alta

            '''
            Política Actual:
            Primero se da de alta: Cuando se terminan los días recomendados en el nivel básico
            '''

            for cama in self.camas_a_dar_de_alta:
                paciente = cama.checkout()

                if isinstance(cama, CamaCritica):
                    dados_alta_critica.append(paciente)

                elif isinstance(cama, CamaIntermedia):
                    dados_alta_intermedia.append(paciente)

                elif isinstance(cama, CamaBasica):
                    dados_alta_basica.append(paciente)

                else:
                    raise Exception("Mala la que haciste")

                # Aprovechamos de guardar estadísticas
                self.dias_extra_c += paciente.dias_extra_c
                self.dias_extra_i += paciente.dias_extra_i



            # ------------------------------------------------------------------
            # Tranferencias de Pacientes entre Camas

            '''
            Política Actual:
            Luego, los pacientes se quedan todo su tiempo recomendado, indpendiente de
            que lleguen a pasar más tiempo.
            PD: Los días extra son días perdidos

            Para evitar Estanque de camas, se intenta transferir a la que tenga
            menor número de días recomendado (Que haya pasado tiempo más cercano al recomendado)
            '''

            # Intermedios
            camas_ordenadas = sorted(self.camas_intermedias_ocupadas,
                                     key = lambda x: x.dias_recomendados)
            #Si quiero poner recomendado tambien hay que modificar la función transferible en la clase Cama para que vea el recomendado y no el minimo
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

            # Críticos
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
                        # No hay camas libres en el nivel intermedio

                        # Acá se debe agregar criterios de transferencia temprana de pacientes

                        break

            # -------------------------------------------------------------------
            # Llegada pacientes

            '''
            Política Actual:
            Si hay una cama en el nivel pedido, se la da. Sino, se externaliza
            '''

            pacientes = pacientes_del_dia(self.tiempo_actual)
            while pacientes:

                # Aumentamos en 1 el número de pacientes que llegan
                self.pacientes_arribados += 1

                paciente = pacientes.popleft()
                if paciente.cama_necesitada == "Critica":
                    camas_libres = self.camas_criticas_libres
                    if len(camas_libres) > 0:
                        # Si hay camas, tomo la primera
                        cama = camas_libres[0]
                        cama.recibir_paciente(paciente)
                    else:
                        # Si no hay camas libres, se externaliza
                        pacientes_externalizados_dia.append(paciente)
                elif paciente.cama_necesitada == "Intermedia":
                    camas_libres = self.camas_intermedias_libres
                    if len(camas_libres) > 0:
                        # Si hay camas, tomo la primera
                        cama = camas_libres[0]
                        cama.recibir_paciente(paciente)
                    else:
                        # Si no hay camas libres, se externaliza
                        pacientes_externalizados_dia.append(paciente)
                else:
                    camas_libres = self.camas_basicas_libres
                    if len(camas_libres) > 0:
                        # Si hay camas, tomo la primera
                        cama = camas_libres[0]
                        cama.recibir_paciente(paciente)
                    else:
                        # Si no hay camas libres, se externaliza
                        pacientes_externalizados_dia.append(paciente)

            # ------------------------------------------------------------------
            # Setup

            self.tiempo_actual += 1
            for cama in self.camas_basicas_ocupadas:
                cama.pasar_dia()
            for cama in self.camas_intermedias_ocupadas:
                cama.pasar_dia()
            for cama in self.camas_criticas_ocupadas:
                cama.pasar_dia()

            self.pacientes_externalizados.append(pacientes_externalizados_dia)
            self.dados_alta_critica.append(dados_alta_critica)
            self.dados_alta_intermedia.append(dados_alta_intermedia)
            self.dados_alta_basica.append(dados_alta_basica)

            ##Nuevas

            dis_critica = (len(self.camas_criticas_libres) * 100) / len(self.camas_criticas)
            dis_intermedia = (len(self.camas_intermedias_libres) * 100) / len(self.camas_intermedias)
            dis_basica = (len(self.camas_basicas_libres) * 100) / len(self.camas_basicas)
            self.disponibilidad.append((dis_critica, dis_intermedia, dis_basica))

        # ------------------------------------------------------------------
        # Termino Simulacion

        self.tiempo_CPU = time() - tiempo_inicio
        #self.show_estadistica()
