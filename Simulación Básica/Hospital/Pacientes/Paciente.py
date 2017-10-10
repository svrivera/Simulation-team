#Creamos la clase Paciente, que es como un puente entre tipo_GRD y la cama (Por eso son puras properties)
class Paciente:

    def __init__(self, fecha_ingreso, GRD):
        self.fecha_ingreso = fecha_ingreso

        self.__GRD = GRD
        GRD.aumentar_contador()

        self.__dias_recomendados_c = GRD.tiempo_recomendado[0]
        self.__dias_recomendados_i = GRD.tiempo_recomendado[1]
        self.dias_recomendados_b = GRD.tiempo_recomendado[2]

        self.dias_minimos_c = GRD.tiempo_minimo[0]
        self.dias_minimos_i = GRD.tiempo_minimo[1]

        self.__dias_adelantado_c = 0
        self.dias_extra_c = 0

        self.__dias_adelantado_i = 0
        self.dias_extra_i = 0

    @property
    def dias_recomendados_c(self):
        return self.__dias_recomendados_c

    @dias_recomendados_c.setter
    def dias_recomendados_c(self, value): #-1
        if value >= 0:
            self.__dias_recomendados_c = value
        else:
            self.dias_extra_c += 1
            self.dias_recomendados_i -= 1
            self.dias_minimos_i -= 1

    @property
    def dias_recomendados_i(self):
        return self.__dias_recomendados_i

    @dias_recomendados_i.setter
    def dias_recomendados_i(self, value):
        if value >= 0:
            self.__dias_recomendados_i = value
        else:
            self.dias_extra_i += 1
            self.dias_recomendados_b -= 1

    @property
    def dias_adelantado_c(self):
        return self.__dias_adelantado_c

    @dias_adelantado_c.setter
    def dias_adelantado_c(self, value):
        if value > 0:
            self.__dias_adelantado_c = value
            self.dias_recomendados_i += value + self.penalizacion_c
            self.dias_recomendados_c = 0
        else:
            self.__dias_adelantado_c = value

    @property
    def dias_adelantado_i(self):
        return self.__dias_adelantado_i

    @dias_adelantado_i.setter
    def dias_adelantado_i(self, value):
        if value > 0:
            self.__dias_adelantado_i = value
            self.dias_recomendados_b += value + self.penalizacion_i
            self.dias_recomendados_i = 0
        else:
            self.__dias_adelantado_i = value

    @property
    def dias_minimos_b(self):
        return self.dias_recomendados_b

    @property
    def tratamiento_restante(self):
        return self.dias_recomendados_c + self.dias_recomendados_i + self.dias_recomendados_b

    @property
    def costo_externalizacion(self):
        return self.__GRD.costo_externalizacion

    @property
    def penalizacion_c(self):
        return self.__GRD.ponderador_c

    @property
    def penalizacion_i(self):
        return self.__GRD.ponderador_i

    @property
    def enfermedad(self):
        return self.__GRD.nombre

    @property
    def cama_necesitada(self):
        if self.dias_minimos_c > 0:
            return "Critica"
        elif self.dias_minimos_i > 0:
            return "Intermedia"
        return "Basica"

    def estadia_hospital(self, dia_actual):
        return dia_actual - self.fecha_ingreso