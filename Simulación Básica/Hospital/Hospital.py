from .Cama import CamaCritica, CamaIntermedia, CamaBasica


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
