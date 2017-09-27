class GRD:
    _id = 0

    def __init__(self):
        self.id = GRD._id
        GRD._id += 1

    @classmethod
    def get_contador(cls):
        return cls.contador

    @classmethod
    def aumentar_contador(cls):
        cls.contador += 1


class Coronario(GRD):
    contador = 0

    def __init__(self):
        self.nombre = "Coronario"
        self.tiempo_recomendado = (3, 4, 4)
        self.tiempo_minimo = (1, 2, 4)
        self.ponderador_c = 3
        self.ponderador_i = 3
        self.costo_externalizacion = 7.53
        super().__init__()


class Hepatico(GRD):
    contador = 0

    def __init__(self):
        self.nombre = "Hepatico"
        self.tiempo_recomendado = (1, 2, 2)
        self.tiempo_minimo = (1, 1, 2)
        self.ponderador_c = 2
        self.ponderador_i = 2
        self.costo_externalizacion = 3.34
        super().__init__()


class Respiratorio(GRD):
    contador = 0

    def __init__(self):
        self.nombre = "Respiratorio"
        self.tiempo_recomendado = (1, 2, 2)
        self.tiempo_minimo = (1, 1, 2)
        self.ponderador_c = 2
        self.ponderador_i = 2
        self.costo_externalizacion = 3.39
        super().__init__()


class Renal(GRD):
    contador = 0

    def __init__(self):
        self.nombre = "Renal"
        self.tiempo_recomendado = (2, 3, 3)
        self.tiempo_minimo = (1, 1, 3)
        self.ponderador_c = 3
        self.ponderador_i = 3
        self.costo_externalizacion = 3.30
        super().__init__()


class Neurologico(GRD):
    contador = 0

    def __init__(self):
        self.nombre = "Neurologico"
        self.tiempo_recomendado = (2, 2, 2)
        self.tiempo_minimo = (1, 1, 2)
        self.ponderador_c = 3
        self.ponderador_i = 3
        self.costo_externalizacion = 3.3
        super().__init__()


class Traumatologico(GRD):
    contador = 0

    def __init__(self):
        self.nombre = "Traumatologico"
        self.tiempo_recomendado = (2, 3, 2)
        self.tiempo_minimo = (1, 2, 2)
        self.ponderador_c = 2
        self.ponderador_i = 2
        self.costo_externalizacion = 4.96
        super().__init__()


class Esofagico(GRD):
    contador = 0

    def __init__(self):
        self.nombre = "Esofagico"
        self.tiempo_recomendado = (0, 2, 2)
        self.tiempo_minimo = (0, 1, 2)
        self.ponderador_c = 0
        self.ponderador_i = 2
        self.costo_externalizacion = 2.81
        super().__init__()


class Oftalmologico(GRD):
    contador = 0

    def __init__(self):
        self.nombre = "Oftalmologico"
        self.tiempo_recomendado = (0, 2, 1)
        self.tiempo_minimo = (0, 1, 1)
        self.ponderador_c = 0
        self.ponderador_i = 1
        self.costo_externalizacion = 2.18
        super().__init__()


class Circulatorio(GRD):
    contador = 0

    def __init__(self):
        self.nombre = "Circulatorio"
        self.tiempo_recomendado = (2, 2, 1)
        self.tiempo_minimo = (1, 1, 1)
        self.ponderador_c = 2
        self.ponderador_i = 2
        self.costo_externalizacion = 2.82
        super().__init__()


class Intestinal(GRD):
    contador = 0

    def __init__(self):
        self.nombre = "Intestinal"
        self.tiempo_recomendado = (0, 4, 4)
        self.tiempo_minimo = (0, 2, 4)
        self.ponderador_c = 0
        self.ponderador_i = 2
        self.costo_externalizacion = 5.25
        super().__init__()


if __name__ == '__main__':
    print(Coronario.contador)