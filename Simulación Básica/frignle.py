from Hospital import HospitalBase, CamaIntermedia, CamaCritica, CamaBasica, pacientes_del_dia
from time import time
from set_politicas import *
from PoliticasTransferencia import *


class Hospital(HospitalBase):


    def __init__(self, tiempo_simulacion, dia_transiente, n_criticas, n_intermedias, n_basicas, cola_paciente):
        super().__init__(tiempo_simulacion, dia_transiente, n_criticas, n_intermedias, n_basicas)
        self.cola_paciente = cola_paciente



    # ----------------------------------------------------------------------------
    def run(self):
        tiempo_inicio = time()
        self.tiempo_actual = 0
        while self.tiempo_actual < self.tiempo_simulacion:

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
                    raise Exception("Mala la que haciste")

                # Aprovechamos de guardar estadísticas
                self.dias_extra_c += paciente.dias_extra_c
                self.dias_extra_i += paciente.dias_extra_i

            # ------------------------------------------------------------------
            # Tranferencias de Pacientes entre Camas
            # Estado del sistema en basica

            n_camas_libres_basicas = len(self.camas_basicas_libres)
            n_transferibles_intermedias = len(self.camas_intermedias_transferible)
            n_transferibles_sin_penalizacion_intermedia = len(self.camas_intermedias_sin_penalizacion)
            n_tranferibles_critica_basica = len(self.camas_criticas_a_basicas)


            # ------------------------------------------------------------------
            #Si nos sobran camas basicas, las bajamos

            #Pasamos intermedia
            if n_camas_libres_basicas >= n_transferibles_intermedias + n_tranferibles_critica_basica + n_transferibles_sin_penalizacion_intermedia:
                bajar_todo_intermedia(self)
                bajar_critica_basica(self)
            else:
                # Estas si que son las politicas
                bajar_critica_basica(self)
                bajar_solo_sin_penalizacion_intermedia(self)
                bajar_todo_intermedia(self)
            # ------------------------------------------------------------------
            # Estado del sistema Critica
            #PARAMETRIZAAAAAR!!!!
            n_llegadas_intermedias = 15
            n_libres_intermedias = len(self.camas_intermedias_libres)
            n_criticas_intermedias = len(self.camas_criticas_a_intermedias)

            # -------------------------------------------------------------------
            #Politicas de vaciado de criticas
            bajar_todo_critica(self)
            # -------------------------------------------------------------------

            dis_critica = (len(self.camas_criticas_libres) * 100) / len(self.camas_criticas)
            dis_intermedia = (len(self.camas_intermedias_libres) * 100) / len(self.camas_intermedias)
            dis_basica = (len(self.camas_basicas_libres) * 100) / len(self.camas_basicas)
            self.disponibilidad_antes.append((dis_critica, dis_intermedia, dis_basica))
            # -------------------------------------------------------------------
            # -------------------------------------------------------------------
            # Llegada pacientes

            #pacientes = pacientes_del_dia(self.tiempo_actual)
            pacientes = self.cola_paciente[self.tiempo_actual]

            # -------------------------------------------------------------------
            # Tratamos a los pacientes
            i=0

            print("comienzo dia")
            print("Pacientes | Disp Critica | # Critica | Disp Intermedia | # Intermedia | Disp Basica | # Basica | Ranking ")


            while pacientes:
                print("{0}         | {1:.4f}     | {2}        | {3:.4f}         | {4}        | {5:.4f}            | {6}     | {7} ".format(i, self.disponibilidad_criticas, len(self.camas_criticas_libres),
                                                                  self.disponibilidad_intermedias, len(self.camas_intermedias_libres),
                                                                  self.disponibilidad_basicas, len(self.camas_basicas_libres),
                                                                self.ranking_promedio))

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
                        politica_exquisita(self, n_llegadas_criticas, n_llegadas_totales, paciente, pacientes_externalizados_dia, camas_libres, self.ranking_promedio,i)

                            # -------------------------------------------------------------------
                    else:
                        # Si no hay camas libres, se externaliza
                        pacientes_externalizados_dia.append(paciente)
                    # diccopnario[estado](self, paciente, pacieete)





                elif paciente.cama_necesitada == "Intermedia":

                    recibir_todo_intermedia(self, paciente, pacientes_externalizados_dia)


                else:

                    recibir_todo_basica(self, paciente, pacientes_externalizados_dia)
                i+=1

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

