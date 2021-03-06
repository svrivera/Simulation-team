#Creamos la clase GRD
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

    @property
    def ranking(self):
        dias_totales = sum(self.tiempo_recomendado)
        if dias_totales == 0:
            return 1
        return self.costo_externalizacion / dias_totales



# Cada tipo de GRD hereda de GRD, los atributos se obtienen de GRDS/__init__.py
class Coronario(GRD):
    contador = 0

    def __init__(self, nombre, tiempo_recomendado, tiempo_minimo, ponderador_c, ponderador_i, costo, tasa):
        self.nombre = nombre
        self.tiempo_recomendado = tiempo_recomendado
        self.tiempo_minimo = tiempo_minimo
        self.ponderador_c = ponderador_c
        self.ponderador_i = ponderador_i
        self.costo_externalizacion = costo
        self.tasa_llegada = tasa
        super().__init__()


class Hepatico(GRD):
    contador = 0

    def __init__(self, nombre, tiempo_recomendado, tiempo_minimo, ponderador_c, ponderador_i, costo, tasa):
        self.nombre = nombre
        self.tiempo_recomendado = tiempo_recomendado
        self.tiempo_minimo = tiempo_minimo
        self.ponderador_c = ponderador_c
        self.ponderador_i = ponderador_i
        self.costo_externalizacion = costo
        self.tasa_llegada = tasa
        super().__init__()


class Respiratorio(GRD):
    contador = 0

    def __init__(self, nombre, tiempo_recomendado, tiempo_minimo, ponderador_c, ponderador_i, costo, tasa):
        self.nombre = nombre
        self.tiempo_recomendado = tiempo_recomendado
        self.tiempo_minimo = tiempo_minimo
        self.ponderador_c = ponderador_c
        self.ponderador_i = ponderador_i
        self.costo_externalizacion = costo
        self.tasa_llegada = tasa
        super().__init__()


class Renal(GRD):
    contador = 0

    def __init__(self, nombre, tiempo_recomendado, tiempo_minimo, ponderador_c, ponderador_i, costo, tasa):
        self.nombre = nombre
        self.tiempo_recomendado = tiempo_recomendado
        self.tiempo_minimo = tiempo_minimo
        self.ponderador_c = ponderador_c
        self.ponderador_i = ponderador_i
        self.costo_externalizacion = costo
        self.tasa_llegada = tasa
        super().__init__()


class Neurologico(GRD):
    contador = 0

    def __init__(self, nombre, tiempo_recomendado, tiempo_minimo, ponderador_c, ponderador_i, costo, tasa):
        self.nombre = nombre
        self.tiempo_recomendado = tiempo_recomendado
        self.tiempo_minimo = tiempo_minimo
        self.ponderador_c = ponderador_c
        self.ponderador_i = ponderador_i
        self.costo_externalizacion = costo
        self.tasa_llegada = tasa
        super().__init__()


class Traumatologico(GRD):
    contador = 0

    def __init__(self, nombre, tiempo_recomendado, tiempo_minimo, ponderador_c, ponderador_i, costo, tasa):
        self.nombre = nombre
        self.tiempo_recomendado = tiempo_recomendado
        self.tiempo_minimo = tiempo_minimo
        self.ponderador_c = ponderador_c
        self.ponderador_i = ponderador_i
        self.costo_externalizacion = costo
        self.tasa_llegada = tasa
        super().__init__()


class Esofagico(GRD):
    contador = 0

    def __init__(self, nombre, tiempo_recomendado, tiempo_minimo, ponderador_c, ponderador_i, costo, tasa):
        self.nombre = nombre
        self.tiempo_recomendado = tiempo_recomendado
        self.tiempo_minimo = tiempo_minimo
        self.ponderador_c = ponderador_c
        self.ponderador_i = ponderador_i
        self.costo_externalizacion = costo
        self.tasa_llegada = tasa
        super().__init__()


class Oftalmologico(GRD):
    contador = 0

    def __init__(self, nombre, tiempo_recomendado, tiempo_minimo, ponderador_c, ponderador_i, costo, tasa):
        self.nombre = nombre
        self.tiempo_recomendado = tiempo_recomendado
        self.tiempo_minimo = tiempo_minimo
        self.ponderador_c = ponderador_c
        self.ponderador_i = ponderador_i
        self.costo_externalizacion = costo
        self.tasa_llegada = tasa
        super().__init__()


class Circulatorio(GRD):
    contador = 0

    def __init__(self, nombre, tiempo_recomendado, tiempo_minimo, ponderador_c, ponderador_i, costo, tasa):
        self.nombre = nombre
        self.tiempo_recomendado = tiempo_recomendado
        self.tiempo_minimo = tiempo_minimo
        self.ponderador_c = ponderador_c
        self.ponderador_i = ponderador_i
        self.costo_externalizacion = costo
        self.tasa_llegada = tasa
        super().__init__()


class Intestinal(GRD):
    contador = 0

    def __init__(self, nombre, tiempo_recomendado, tiempo_minimo, ponderador_c, ponderador_i, costo, tasa):
        self.nombre = nombre
        self.tiempo_recomendado = tiempo_recomendado
        self.tiempo_minimo = tiempo_minimo
        self.ponderador_c = ponderador_c
        self.ponderador_i = ponderador_i
        self.costo_externalizacion = costo
        self.tasa_llegada = tasa
        super().__init__()


if __name__ == '__main__':
    print(Coronario.contador)