#Creamos la clase Paciente, que es como un puente entre tipo_GRD y la cama (Por eso son puras properties)
class Paciente:

    def __init__(self, fecha_ingreso, GRD):
        self.fecha_ingreso = fecha_ingreso
        self.__GRD = GRD
        self.__GRD.aumentar_contador()

        self.dias_adelantado_c = 0
        self.dias_extra_c = 0

        self.dias_adelantado_i = 0
        self.dias_extra_i = 0

    @property
    def costo_externalizacion(self):
        return self.__GRD.costo_externalizacion

    @property
    def ponderador_c(self):
        return self.__GRD.ponderador_c

    @property
    def ponderador_i(self):
        return self.__GRD.ponderador_i

    @property
    def enfermedad(self):
        return self.__GRD.nombre

    @property
    def penalizacion_critica(self):
        return self.dias_adelantado_c * self.ponderador_c

    @property
    def penalizacion_intermedia(self):
        return self.dias_adelantado_i * self.ponderador_i

    @property
    def dias_minimo_critica(self):
        return self.__GRD.tiempo_minimo[0]

    @property
    def dias_minimo_intermedia(self):
        return self.__GRD.tiempo_minimo[1]

    @property
    def dias_minimo_basica(self):
        return self.__GRD.tiempo_minimo[2]

    @property
    def dias_recomendado_critica(self):
        return self.__GRD.tiempo_recomendado[0]

    @property
    def dias_recomendado_intermedia(self):
        return self.__GRD.tiempo_recomendado[1]

    @property
    def dias_recomendado_basica(self):
        return self.__GRD.tiempo_recomendado[2]

    @property
    def cama_inicial(self):
        if self.dias_recomendado_critica > 0:
            return "Critica"
        if self.dias_recomendado_intermedia > 0:
            return "Intermedia"
        return "Basica"

    @property
    def estadia_hospital(self, dia_actual):
        return dia_actual - self.fecha_ingreso