from Hospital import HospitalBase, CamaIntermedia, CamaCritica, CamaBasica, pacientes_del_dia,  llegadas_esperadas_criticas, llegadas_esperadas_intermedias, deseados_criticos, deseados_intermedias
from time import time
from set_politicas import *
from PoliticasTransferencia import *
from Estado import calcular_estado_sistema_transferencia, calcular_estado_recibir_intermedia
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

                else:
                    raise Exception("Red Wifi UC no encontrada...")

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
            if n_camas_libres_basicas >= n_transferibles_intermedias + n_tranferibles_critica_basica + n_transferibles_sin_penalizacion_intermedia:
                bajar_todo_intermedia(self)
                bajar_critica_basica(self)
            else:
                # Estas si que son las politicas
                bajar_critica_basica(self)
                bajar_solo_sin_penalizacion_intermedia(self)
                bajar_todo_intermedia(self)

            # ------------------------------------------------------------------
            ## Transferencia HACIA Intermedia:

            bajar_todo_critica(self, boolean = False)
            #print(self.disponibilidad_criticas)
            # ------------------------------------------------------------------
            # LLEGADA PACIENTES


            pacientes = self.cola_paciente[self.tiempo_actual]

            # -------------------------------------------------------------------
            # Tratamos a los pacientes
            avanzados = 0

            llegadas = defaultdict(int)

            #print("comienzo dia")
            #print("Pacientes | Disp Critica | # Critica | Disp Intermedia | # Intermedia | Disp Basica | # Basica | Ranking ")


            while pacientes:

                paciente = pacientes.popleft()
                # Calculamos estado del sistema
                # --------------------------------------------------
                # PARAMETRIZAR LLEGADAS DIARIAS PAL QUE NO CACHA, EL 35
                n_llegadas_criticas = 35
                n_llegadas_totales = 50

                # -------------------------------------------------------------------
                # Aumentamos en 1 el número de pacientes que llegan
                self.pacientes_arribados += 1
                if paciente.cama_necesitada == "Critica":

                    camas_libres = self.camas_criticas_libres
                    if len(camas_libres) > 0:
                        # Buscamos politicas segun estado estoy intentando implementar la politica exquisita un manjar
                        # -------------------------------------------------------------------
                        # Jugamos
                        recibir_todo_critica(self, paciente, camas_libres[0])
                            # -------------------------------------------------------------------
                    else:
                        # Si no hay camas libres, se externaliza
                        pacientes_externalizados_dia.append(paciente)


                elif paciente.cama_necesitada == "Intermedia":

                    camas_libres = self.camas_intermedias_libres
                    if len(camas_libres) > 0:
                        self.p_intermedios += 1
                        recibir_todo_intermedia(self, paciente, camas_libres[0])
                    else:
                        # Si no hay camas libres, se externaliza
                        pacientes_externalizados_dia.append(paciente)


                else:

                    recibir_todo_basica(self, paciente, pacientes_externalizados_dia)


                avanzados+=1

                llegadas[paciente.enfermedad] += 1
            #print(self.disponibilidad_criticas)
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

