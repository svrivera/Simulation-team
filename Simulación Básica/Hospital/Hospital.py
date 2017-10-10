from time import time
from .Cama import CamaCritica, CamaIntermedia, CamaBasica
from .Pacientes import pacientes_del_dia, n_hepaticos, n_circulatorio, \
    n_coronarios, n_esofagico, n_intestinal, n_neurologico, n_oftalmologico, \
    n_renal, n_respiratorio, n_traumatologico


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

        self.dados_alta_critica = []
        self.dados_alta_intermedia = []
        self.dados_alta_basica = []


        self.dias_extra_c = 0
        self.dias_extra_i = 0
        self.pacientes_arribados = 0

        self.disponibilidad = []

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
    def camas_a_dar_de_alta(self):
        l1 = list(filter(lambda x: x.alta_medica, self.camas_criticas_ocupadas))
        l2 = list(filter(lambda x: x.alta_medica, self.camas_intermedias_ocupadas))
        l3 = list(filter(lambda x: x.alta_medica, self.camas_basicas_ocupadas))
        return l1 + l2 + l3

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


    # ----------------------------------------------------------------------------
    # creamos los parametros:

    @property
    def costo_externalizacion(self):
        return sum(map(lambda x: sum(map(lambda y: y.costo_externalizacion, x)),
                                                               self.pacientes_externalizados))
    @property
    def pacientes_derivados(self):
        return sum(map(lambda x: len(x), self.pacientes_externalizados))

    @property
    def altas_dadas_critica(self):
        return sum(map(lambda x: len(x), self.dados_alta_critica))

    @property
    def altas_dadas_intermedia(self):
        return sum(map(lambda x: len(x), self.dados_alta_intermedia))

    @property
    def altas_dadas_basica(self):
        return sum(map(lambda x: len(x), self.dados_alta_basica))


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
                    raise Exception("Ta la cagaa")

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

    def show_estadistica(self):
        s = ""
        s += "Simulación [{}]\n\n".format(self.id)
        s += "Tiempo de Simulación: {}\n".format(self.tiempo_CPU)
        s += "Días Simulados: {}\n".format(self.tiempo_simulacion)
        s += "Costo Externalización Total: {}\n".format(self.costo_externalizacion)
        s += "Cantidad de Pacientes Derivados: {}\n".format(self.pacientes_derivados)
        s += "Cantidad de Pacientes dados de Alta: {}\n".format(self.altas_dadas)

        s += "Días Perdidos:\n"
        s += "Días Totales Perdidos en Críticas: {}\n".format(self.dias_extra_c)
        s += "Días Totales Perdidos en Intermedias: {}\n".format(self.dias_extra_i)
        s += "Estado Sistema al finalizar\n"
        s += "Cantidad de Camas Críticas Ocupadas: {}\n".format(len(self.camas_criticas_ocupadas))
        s += "Cantidad de Camas Intermedias Ocupadas: {}\n".format(len(self.camas_intermedias_ocupadas))
        s += "Cantidad de Camas Básicas Ocupadas: {}\n".format(len(self.camas_basicas_ocupadas))
        # print(n_hepaticos())
        # print(self.pacientes_arribados)
        # print(len(self.camas_criticas_ocupadas))


        print(s)
