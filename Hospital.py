from time import time
from Cama import CamaCritica, CamaIntermedia, CamaBasica
from Paciente import Paciente
from GRDS import *
from numpy.random import poisson
from random import shuffle
from collections import deque


class Hospital:

    _id = 0

    def __init__(self, tiempo_simulacion, n_criticas, n_intermedias, n_basicas):
        self.id = Hospital._id
        Hospital._id += 1

        self.tiempo_simulacion = tiempo_simulacion
        self.tiempo_actual = 0
        self.tiempo_CPU = 0

        # Construimos las camas
        self.camas_criticas = []
        self.camas_intermedias = []
        self.camas_basicas = []
        self.construir_hospital(n_criticas, n_intermedias, n_basicas)

        # Estadisticas
        self.pacientes_externalizados = []
        self.pacientes_dados_alta = []
        self.dias_extra_c = 0
        self.dias_extra_i = 0
        self.pacientes_arribados = 0

        '''
        pacientes derivados
        pacientes atendidos de cada tipo
        diferencia promedio de dias de tralado de tiempo reomencada
        costos total externalizacion
        dias extra por cada nivel

        '''

    def construir_hospital(self, n_criticas, n_intermedias, n_basicas):
        for i in range(n_criticas):
            self.camas_criticas.append(CamaCritica())
        for i in range(n_intermedias):
            self.camas_intermedias.append(CamaIntermedia())
        for i in range(n_basicas):
            self.camas_basicas.append(CamaBasica())

    # ---------------------------------------------------------------------------

    @property
    def camas_criticas_ocupadas(self):
        return list(filter(lambda x: not x.libre, self.camas_criticas))

    @property
    def camas_intermedias_ocupadas(self):
        return list(filter(lambda x: not x.libre, self.camas_intermedias))

    @property
    def camas_basicas_ocupadas(self):
        return list(filter(lambda x: not x.libre, self.camas_basicas))

    # ---------------------------------------------------------------------------

    @property
    def camas_criticas_libres(self):
        return list(filter(lambda x: x.libre, self.camas_criticas))

    @property
    def camas_intermedias_libres(self):
        return list(filter(lambda x: x.libre, self.camas_intermedias))

    @property
    def camas_basicas_libres(self):
        return list(filter(lambda x: x.libre, self.camas_basicas))

    # ---------------------------------------------------------------------------

    @property
    def camas_criticas_transferible(self):
        return list(filter(lambda x: x.transferible, self.camas_criticas_ocupadas))

    @property
    def camas_intermedias_transferible(self):
        return list(filter(lambda x: x.transferible, self.camas_intermedias_ocupadas))

    # ---------------------------------------------------------------------------
#####  Política: Mejor cama para transferir es la que da menos penalización

    @property
    def mejor_cama_critica_trasferible(self):
        return sorted(self.camas_criticas_transferible,
                      key = lambda x: x.tiempo_posible_penalizacion)[0]

    @property
    def mejor_cama_intermedia_trasferible(self):
        return sorted(self.camas_intermedias_transferible,
                      key = lambda x: x.tiempo_posible_penalizacion)[0]

    # ---------------------------------------------------------------------------
    # Creación de la cola de Pacientes que llegan en el día

    def pacientes_del_dia(self):
        pacientes = []
        lista = [GRD_Coronario,
                GRD_Hepatico,
                GRD_Respiratorio,
                GRD_Renal,
                GRD_Neurologico,
                GRD_Traumatologico,
                GRD_Esofagico,
                GRD_Oftalmologico,
                GRD_Circulatorio,
                GRD_Intestinal]
        for grd in lista:
            for i in range(poisson(5)):
                pacientes.append(Paciente(self.tiempo_actual, grd))
        shuffle(pacientes)
        return deque(pacientes)

    # ---------------------------------------------------------------------------


    def run(self):
        tiempo_inicio = time()

        while self.tiempo_actual < self.tiempo_simulacion:

            # -------------------------------------------------------------------
            # Setup Inicial del dia
            pacientes_externalizados_dia = []
            pacientes_dados_alta_dia = []

            # ------------------------------------------------------------------
            # Dar de alta

            '''
            Política Actual:
            Se da de alta cuando se terminan los días recomendados en el nivel básico
            '''

            for cama in self.camas_basicas_ocupadas:
                if cama.alta_medica:
                    paciente = cama.checkout()
                    pacientes_dados_alta_dia.append(paciente)

                    # Aprovechamos de guardar estadísticas
                    self.dias_extra_c += paciente.dias_extra_c
                    self.dias_extra_i += paciente.dias_extra_i

            # ------------------------------------------------------------------
            # Tranferencias de Pacientes entre Camas

            '''
            Política Actual:
            Pacientes se quedan todo su tiempo recomendado, indpendiente de
            que lleguen a pasar más tiempo.
            PD: Los días extra son días perdidos

            Para evitar MUERTE de camas, se intenta transferir a la que tenga
            menor número de días recomendado (NUESTRO)
            '''

            # Intermedios
            camas_ordenadas = sorted(self.camas_intermedias_ocupadas,
                                     key = lambda x: x.dias_recomendado)
            for cama_origen in camas_ordenadas:
                if cama_origen.dias_recomendado <= 0:
                    camas_libres = self.camas_basicas_libres
                    if len(camas_libres) > 0:
                        # Si hay camas, tomo la primera
                        cama_destino = camas_libres[0]
                        paciente = cama_origen.checkout()
                        cama_destino.recibir_paciente(paciente)
                    else:
                        # No hay camas libres en el próximo nivel
                        break

            # Críticos
            camas_ordenadas = sorted(self.camas_criticas_ocupadas,
                                     key=lambda x: x.dias_recomendado)
            for cama_origen in camas_ordenadas:
                if cama_origen.dias_recomendado <= 0:
                    camas_libres = self.camas_intermedias_libres
                    if len(camas_libres) > 0:
                        # Si hay camas, tomo la primera
                        cama_destino = camas_libres[0]
                        paciente = cama_origen.checkout()
                        cama_destino.recibir_paciente(paciente)
                    else:
                        # No hay camas libres en el próximo nivel
                        break

            # -------------------------------------------------------------------
            # Llegada pacientes

            '''
            Política Actual:
            Si hay una cama en el nivel pedido, se la da. Sino, se externaliza
            '''

            pacientes = self.pacientes_del_dia()
            while pacientes:

                # Aumentamos en 1 el número de pacientes que llegan
                self.pacientes_arribados += 1

                paciente = pacientes.popleft()
                if paciente.cama_inicial == "Critica":
                    camas_libres = self.camas_criticas_libres
                    if len(camas_libres) > 0:
                        # Si hay camas, tomo la primera
                        cama = camas_libres[0]
                        cama.recibir_paciente(paciente)
                    else:
                        # Si no hay camas libres, se externaliza
                        pacientes_externalizados_dia.append(paciente)
                elif paciente.cama_inicial == "Intermedia":
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
            self.pacientes_dados_alta.append(pacientes_dados_alta_dia)

        # ------------------------------------------------------------------
        # Termino Simulacion

        self.tiempo_CPU = time() - tiempo_inicio

        self.show_estadistica()

    def show_estadistica(self):
        s = ""
        s += "Simulación [{}]\n\n".format(self.id)
        s += "Tiempo de Simulación: {}\n".format(self.tiempo_CPU)
        s += "Días Simulados: {}\n".format(self.tiempo_simulacion)
        s += "Costo Externalización Total: {}\n".format(sum(map(lambda x: sum(map(lambda y: y.costo_externalizacion, x)),
                                                               self.pacientes_externalizados)))
        s += "Cantidad de Pacientes Derivados: {}\n".format(sum(map(lambda x: len(x), self.pacientes_externalizados)))
        s += "Cantidad de Pacientes dados de Alta: {}\n".format(sum(map(lambda x: len(x), self.pacientes_dados_alta)))

        s += "Días Perdidos:\n"
        s += "Días Totales Perdidos en Críticas: {}\n".format(self.dias_extra_c)
        s += "Días Totales Perdidos en Intermedias: {}\n".format(self.dias_extra_i)
        s += "Estado Sistema al finalizar\n"
        s += "Cantidad de Camas Críticas Ocupadas: {}\n".format(len(self.camas_criticas_ocupadas))
        s += "Cantidad de Camas Intermedias Ocupadas: {}\n".format(len(self.camas_intermedias_ocupadas))
        s += "Cantidad de Camas Básicas Ocupadas: {}\n".format(len(self.camas_basicas_ocupadas))

        # print(self.pacientes_arribados)
        # print(len(self.camas_criticas_ocupadas))

        print(s)