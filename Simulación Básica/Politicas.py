from Hospital import HospitalBase, CamaIntermedia, CamaCritica, CamaBasica, pacientes_del_dia,  llegadas_esperadas_criticas, llegadas_esperadas_intermedias, deseados_criticos, deseados_intermedias
from time import time
from set_politicas import *
from PoliticasTransferencia import *
from Estado import *
from collections import defaultdict


class Hospital(HospitalBase):


    def __init__(self, tiempo_simulacion, dia_transiente, n_criticas, n_intermedias, n_basicas, cola_paciente,
                 politica_hacia_intermedia, politicas_llegadas_intermedias):
        super().__init__(tiempo_simulacion, dia_transiente, n_criticas, n_intermedias, n_basicas)
        self.cola_paciente = cola_paciente
        self.politica_hacia_intermedia = politica_hacia_intermedia
        self.politicas_llegadas_intermedias = politicas_llegadas_intermedias
        self.p_intermedios = 0


    # ----------------------------------------------------------------------------
    def run(self):
        tiempo_inicio = time()

        while self.tiempo_actual < self.tiempo_simulacion + self.dia_transiente:

            # -------------------------------------------------------------------
            # Setup Inicial del dia
            pacientes_externalizados_dia = []
            dados_alta_critica = []
            dados_alta_intermedia = []
            dados_alta_basica = []
            # ------------------------------------------------------------------
            # Dar de alta a toodo el hospital

            for cama in self.camas_a_dar_de_alta:
                paciente = cama.checkout()

                if isinstance(cama, CamaCritica):
                    dados_alta_critica.append(paciente)

                elif isinstance(cama, CamaIntermedia):
                    dados_alta_intermedia.append(paciente)

                elif isinstance(cama, CamaBasica):
                    dados_alta_basica.append(paciente)

                # Aprovechamos de guardar estadísticas
                self.dias_extra_c += paciente.dias_extra_c
                self.dias_extra_i += paciente.dias_extra_i

            # ------------------------------------------------------------------
            # ------------------------------------------------------------------
            # ------------------------------------------------------------------
            ##### Tranferencias de Pacientes entre Camas #####

            # ------------------------------------------------------------------
            ## Transferencia HACIA basica:

            # Estado del sistema en basica

            n_camas_libres_basicas = len(self.camas_basicas_libres)
            n_transferibles_intermedias = len(self.camas_intermedias_transferible)
            n_transferibles_sin_penalizacion_intermedia = len(self.camas_intermedias_sin_penalizacion)
            n_tranferibles_critica_basica = len(self.camas_criticas_a_basicas)

            # Pasamos intermedia
            if n_camas_libres_basicas >= n_transferibles_intermedias + n_tranferibles_critica_basica:
                bajar_critica_basica(self)
                bajar_todo_intermedia(self)

            else:
                # Estas si que son las politicas
                bajar_critica_basica(self)
                bajar_solo_sin_penalizacion_intermedia(self)
                bajar_todo_intermedia(self)

            # ------------------------------------------------------------------
            ## Transferencia HACIA Intermedia:

            n_camas_libres_intermedia = len(self.camas_intermedias_libres)
            n_transferibles_criticas = len(self.camas_criticas_transferible)
            n_transferibles_sin_penalizacion_critica = len(self.camas_criticas_sin_penalizacion)

            # llegadas_esperadas_intermedias: estimado de llegadas (~15)

            estado = calcular_estado_sistema_transferencia(self.disponibilidad_criticas, self.disponibilidad_intermedias)
            self.politica_hacia_intermedia[estado](self, llegadas_esperadas_intermedias, 2)

            #print("Disp Critica | # Critica | Disp Intermedia | # Intermedia | Disp Basica | # Basica | Ranking ")
            #print("{0:.4f}     | {1}        | {2:.4f}         | {3}        | {4:.4f}            | {5}     | {6} ".format(
            #        self.disponibilidad_criticas, len(self.camas_criticas_libres),
            #        self.disponibilidad_intermedias, len(self.camas_intermedias_libres),
            #        self.disponibilidad_basicas, len(self.camas_basicas_libres),
            #        self.ranking_promedio))
            #bajar_con_reserva_moderada
            #print("Disp Critica | # Critica | Disp Intermedia | # Intermedia | Disp Basica | # Basica | Ranking ")
            #print("{0:.4f}     | {1}        | {2:.4f}         | {3}        | {4:.4f}            | {5}     | {6} ".format(
            #        self.disponibilidad_criticas, len(self.camas_criticas_libres),
            #        self.disponibilidad_intermedias, len(self.camas_intermedias_libres),
            #        self.disponibilidad_basicas, len(self.camas_basicas_libres),
            #        self.ranking_promedio))
            #print("-------"*10)

            # ------------------------------------------------------------------



            # ------------------------------------------------------------------
            # LLEGADA PACIENTES


            pacientes = self.cola_paciente[self.tiempo_actual]

            # -------------------------------------------------------------------
            # Tratamos a los pacientes
            avanzados=0

            llegadas = defaultdict(int)

            #print("comienzo dia")
            #print("Pacientes | Disp Critica | # Critica | Disp Intermedia | # Intermedia | Disp Basica | # Basica | Ranking ")


            while pacientes:
                #print("{0}         | {1:.4f}     | {2}        | {3:.4f}         | {4}        | {5:.4f}            | {6}     | {7} ".format(avanzados, self.disponibilidad_criticas, len(self.camas_criticas_libres),
                #                                                 self.disponibilidad_intermedias, len(self.camas_intermedias_libres),
                #                                                  self.disponibilidad_basicas, len(self.camas_basicas_libres),
                #                                                self.ranking_promedio))

                paciente = pacientes.popleft()
                # Calculamos estado del sistema
                # --------------------------------------------------
                n_llegadas_criticas = 35
                n_llegadas_totales = 50


                #deseados_intermedio = deseados_intermedias(self.ranking_promedio)
                deseados_intermedio = ["Esofagico", "Oftalmologico"]



                n_deseados_ya_arribados_intermedio = sum(llegadas[x] for x in deseados_intermedio)
                estado_intermedio = calcular_estado_recibir_intermedia(self.disponibilidad_intermedias, avanzados, 5 * len(deseados_intermedio),
                                                                       n_deseados_ya_arribados_intermedio)
                #print("Estado Intermedio:", estado_intermedio)

                # -------------------------------------------------------------------
                # Aumentamos en 1 el número de pacientes que llegan
                self.pacientes_arribados += 1
                if paciente.cama_necesitada == "Critica":


                    deseados = deseados_criticos(self.ranking_promedio)
                    deseados_arribados = sum(llegadas[x] for x in deseados)


                    camas_libres = self.camas_criticas_libres
                    if len(camas_libres) > 0:
                        # Buscamos politicas segun estado estoy intentando implementar la politica exquisita un manjar
                        # -------------------------------------------------------------------
                        # Jugamos
                        estado = calcular_estado_recibir_critica(self.disponibilidad_criticas, avanzados, 5 * len(deseados), deseados_arribados)
                        politicas_llegadas_criticas[estado](self, paciente, camas_libres[0], pacientes_externalizados_dia, self.ranking_promedio)

                            # -------------------------------------------------------------------
                    else:
                        # Si no hay camas libres, se externaliza
                        pacientes_externalizados_dia.append(paciente)
                    # diccopnario[estado](self, paciente, pacieete)





                elif paciente.cama_necesitada == "Intermedia":


                    camas_libres = self.camas_intermedias_libres

                    #print(deseados, self.ranking_promedio, len(camas_libres) > 0)
                    if len(camas_libres) > 0:
                        # Parametrizar el 10
                        self.p_intermedios += 1
                        self.politicas_llegadas_intermedias[estado_intermedio](self, paciente, camas_libres[0], pacientes_externalizados_dia, deseados_intermedio)
                    else:
                        # Si no hay camas libres, se externaliza
                        pacientes_externalizados_dia.append(paciente)


                else:

                    recibir_todo_basica(self, paciente, pacientes_externalizados_dia)


                avanzados+=1

                llegadas[paciente.enfermedad] += 1

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

            dis_critica = self.disponibilidad_criticas
            dis_intermedia = self.disponibilidad_intermedias
            dis_basica = self.disponibilidad_basicas
            self.disponibilidad.append((dis_critica, dis_intermedia, dis_basica))


        # ------------------------------------------------------------------
        # Termino Simulacion

        self.tiempo_CPU_preparacion = time() - tiempo_inicio
        # self.show_estadistica()

