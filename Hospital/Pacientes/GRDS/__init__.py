from .GRD import *


# Abrir archivo e instanciar las cosas con los valores respectivos


GRD_Coronario = Coronario(nombre="Coronario", tiempo_recomendado=(3, 4, 4), tiempo_minimo=(1, 2, 4), ponderador_c=3,
                          ponderador_i=3, costo=7.53, tasa=5.288)
GRD_Hepatico = Hepatico("Hepatico", (1, 2, 2), (1, 1, 2), 2, 2, 3.34, tasa=5.188)
GRD_Respiratorio = Respiratorio("Respiratorio", (1, 2, 2), (1, 1, 2), 2, 2, 3.39, tasa=5.12)
GRD_Renal = Renal("Renal", (2, 3, 3), (1, 1, 3), 3, 3, 3.30, tasa=5.051)
GRD_Neurologico = Neurologico("Neurologico", (2, 2, 2), (1, 1, 2), 3, 3, 3.3, tasa=5.188)
GRD_Traumatologico = Traumatologico("Traumatologico", (2, 3, 2), (1, 2, 2), 2, 2, 4.96, tasa=5.094)
GRD_Esofagico = Esofagico("Esofagico", (0, 2, 2), (0, 1, 2), 0, 2, 2.81, tasa=5.048)
GRD_Oftalmologico = Oftalmologico("Oftalmologico", (0, 2, 1), (0, 1, 1), 0, 1, 2.18, tasa=5.168)
GRD_Circulatorio = Circulatorio("Circulatorio", (2, 2, 1), (1, 1, 1), 2, 2, 2.82, tasa=5.237)
GRD_Intestinal = Intestinal("Intestinal", (0, 4, 4), (0, 2, 4), 0, 2, 5.25, tasa=4.985)

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

# Cargamos las tasas de llegada de cada GRD

