"""Tiene un paciente y cuando este llega se actualizan los parámetros dias_minimo y recomendados, luego con cada día de
    simulación que pasa, se le resta a los días"""


class Cama:
    def __init__(self):
        self.paciente = None

    # Lo siguiente puede ser útil para asignar políticas:
    # ---------------------------------------------------

    @property
    def libre(self):
        return self.paciente is None

    @property
    def ocupada(self):
        return self.paciente is not None

    # ---------------------------------------------------

    @property
    def enfermedad(self):
        return self.paciente.enfermedad

    @property
    def alta_medica(self):
        return self.paciente.tratamiento_restante <= 0

    def pasar_dia(self):
        self.dias_minimos -= 1
        self.dias_recomendados -= 1

    def recibir_paciente(self, paciente):
        self.paciente = paciente

# Cada tipo de cama va asignada a una etapa del tratamiento del paciente
class CamaCritica(Cama):

    def __init__(self):
        super().__init__()

    @property
    def dias_minimos(self):
        return self.paciente.dias_minimos_c

    @dias_minimos.setter
    def dias_minimos(self, value):
        self.paciente.dias_minimos_c = value

    @property
    def dias_recomendados(self):
        return self.paciente.dias_recomendados_c

    @dias_recomendados.setter
    def dias_recomendados(self, value):
        self.paciente.dias_recomendados_c = value

    @property
    def transferible(self):
        return self.paciente.dias_minimos_c <= 0

    def checkout(self):
        paciente = self.paciente

        if self.dias_recomendados >= 0:
            paciente.dias_adelantado_c = self.dias_recomendados
        else:
            #sasaasasas
            paciente.dias_extra_c = abs(self.dias_recomendados)
        self.paciente = None
        return paciente

class CamaIntermedia(Cama):
    def __init__(self):
        super().__init__()

    @property
    def dias_minimos(self):
        return self.paciente.dias_minimos_i

    @dias_minimos.setter
    def dias_minimos(self, value):
        self.paciente.dias_minimos_i = value

    @property
    def dias_recomendados(self):
        return self.paciente.dias_recomendados_i

    @dias_recomendados.setter
    def dias_recomendados(self, value):
        self.paciente.dias_recomendados_i = value

    @property
    def transferible(self):
        return self.paciente.dias_minimos_i <= 0

    def checkout(self):
        paciente = self.paciente

        if self.dias_recomendados >= 0:
            paciente.dias_adelantado_i += self.dias_recomendados
            # paciente.dias_extra_i = 0
        else:
            # paciente.dias_adelantado_i = 0
            paciente.dias_extra_i += abs(self.dias_recomendados)
        self.paciente = None
        return paciente

# Solo la cama básica puede dar de alta al paciente
class CamaBasica(Cama):
    def __init__(self):
        super().__init__()

    @property
    def dias_minimos(self):
        return self.paciente.dias_minimos_b

    @dias_minimos.setter
    def dias_minimos(self, value):
        self.paciente.dias_minimos_b = value

    @property
    def dias_recomendados(self):
        return self.paciente.dias_recomendados_b

    @dias_recomendados.setter
    def dias_recomendados(self, value):
        self.paciente.dias_recomendados_b = value

    def checkout(self):
        paciente = self.paciente
        self.paciente = None
        return paciente

    def pasar_dia(self):
        self.dias_recomendados -= 1
