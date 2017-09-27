from .GRD import *


# Abrir archivo e instanciar las cosas con los valores respectivos

# GRD_Coronario = Coronario(1,4,6,7,88,8)
GRD_Coronario = Coronario()
GRD_Hepatico = Hepatico()
GRD_Respiratorio = Respiratorio()
GRD_Renal = Renal()
GRD_Neurologico = Neurologico()
GRD_Traumatologico = Traumatologico()
GRD_Esofagico = Esofagico()
GRD_Oftalmologico = Oftalmologico()
GRD_Circulatorio = Circulatorio()
GRD_Intestinal = Intestinal()

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

