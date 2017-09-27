__author__ = "Ale, Seba y Benja <3"

class Cama:
    def __init__(self):
        self.paciente = None
        self.dias_minimos = 0
        self.dias_recomendado = 0

        self.reservada_hasta = 0  # todavía no lo usamos

    # Lo podemos usar más adelante con una política
    @property
    def reservada(self):
        return self.reservada_hasta > 0

    @property
    def libre(self):
        return self.paciente is None

    @property
    def trasferible(self):
        return self.dias_minimos <= 0

    @property
    def enfermedad(self):
        return self.paciente.enfermedad

    def pasar_dia(self):
        self.dias_minimos -= 1
        self.dias_recomendado -= 1


class CamaCritica(Cama):

    def __init__(self):
        super().__init__()

    @property
    def tiempo_posible_penalizacion(self):
        return self.dias_recomendado * self.paciente.ponderador_c

    def checkout(self):
        paciente = self.paciente
        self.paciente = None
        if self.dias_recomendado >= 0:
            paciente.dias_adelantado_c += self.dias_recomendado
            # paciente.dias_extra_c = 0
        else:
            # paciente.dias_adelantado_c = 0
            paciente.dias_extra_c += abs(self.dias_recomendado)
        self.dias_recomendado = 0
        self.dias_minimos = 0
        return paciente

    def recibir_paciente(self, paciente):
        self.paciente = paciente
        self.dias_minimos = paciente.dias_minimo_critica
        self.dias_recomendado = paciente.dias_recomendado_critica


class CamaIntermedia(Cama):
    def __init__(self):
        super().__init__()

    @property
    def tiempo_posible_penalizacion(self):
        return self.dias_recomendado * self.paciente.ponderador_i

    def checkout(self):
        paciente = self.paciente
        self.paciente = None
        if self.dias_recomendado >= 0:
            paciente.dias_adelantado_i += self.dias_recomendado
            # paciente.dias_extra_i = 0
        else:
            # paciente.dias_adelantado_i = 0
            paciente.dias_extra_i += abs(self.dias_recomendado)
        self.dias_recomendado = 0
        self.dias_minimos = 0
        return paciente

    def recibir_paciente(self, paciente):
        self.paciente = paciente
        self.dias_minimos = paciente.dias_minimo_intermedia + paciente.penalizacion_critica
        self.dias_recomendado = paciente.dias_recomendado_intermedia + paciente.penalizacion_critica


class CamaBasica(Cama):
    def __init__(self):
        super().__init__()

    @property
    def alta_medica(self):
        return self.dias_recomendado <= 0

    def checkout(self):
        self.dias_minimos = 0
        self.dias_recomendado = 0
        paciente = self.paciente
        self.paciente = None
        return paciente

    def recibir_paciente(self, paciente):
        self.paciente = paciente
        self.dias_minimos = paciente.dias_minimo_basica + paciente.penalizacion_intermedia
        self.dias_recomendado = paciente.dias_recomendado_basica + paciente.penalizacion_intermedia


