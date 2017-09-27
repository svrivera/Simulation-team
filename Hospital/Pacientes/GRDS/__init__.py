from .GRD import *


# Abrir archivo e instanciar las cosas con los valores respectivos


GRD_Coronario = Coronario(nombre="Coronario", tiempo_recomendado=(3, 4, 4), tiempo_minimo=(1, 2, 4), ponderador_c=3,
                          ponderador_i=3, costo_externalizacion=7.53)
GRD_Hepatico = Hepatico("Hepatico", (1, 2, 2), (1, 1, 2), 2, 2, 3.34)
GRD_Respiratorio = Respiratorio("Respiratorio", (1, 2, 2), (1, 1, 2), 2, 2, 3.39)
GRD_Renal = Renal("Renal", (2, 3, 3), (1, 1, 3), 3, 3, 3.30)
GRD_Neurologico = Neurologico("Neurologico", (2, 2, 2), (1, 1, 2), 3, 3, 3.3)
GRD_Traumatologico = Traumatologico("Traumatologico", (2, 3, 2), (1, 2, 2), 2, 2, 4.96)
GRD_Esofagico = Esofagico("Esofagico", (0, 2, 2), (0, 1, 2), 0, 2, 2.81)
GRD_Oftalmologico = Oftalmologico("Oftalmologico", (0, 2, 1), (0, 1, 1), 0, 1, 2.18)
GRD_Circulatorio = Circulatorio("Circulatorio", (2, 2, 1), (1, 1, 1), 2, 2, 2.82)
GRD_Intestinal = Intestinal("Intestinal", (0, 4, 4), (0, 2, 4), 0, 2, 5.25)

# Guardamos las funciones en un nombre más entendible

n_coronarios = Coronario.get_contador
n_hepaticos = Hepatico.get_contador
n_respiratorio = Respiratorio.get_contador
n_renal = Renal.get_contador
n_neurologico = Neurologico.get_contador
n_traumatologico = Traumatologico.get_contador
n_esofagico = Esofagico.get_contador
n_oftalmologico = Oftalmologico.get_contador
n_circulatorio = Circulatorio.get_contador
n_intestinal = Intestinal.get_contador

