class GRD:
    def __init__(self, id, nombre, trc, tri, trb, tmc, tmi, tmb,
                 ponderador_c, ponderador_i, costo_externalizacion):
        self.id = id
        self.nombre = nombre
        self.tiempo_recomendado = (trc, tri, trb)
        self.tiempor_minimo = (tmc, tmi, tmb)
        self.ponderador_c = ponderador_c
        self.ponderador_i = ponderador_i
        self.costo_externalizacion = costo_externalizacion


