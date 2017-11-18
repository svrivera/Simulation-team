
from numpy.random import poisson
import json
from random import shuffle


NOMBRE_ARCHIVO = "colas.json"

tasas = {}
tasas["Coronario"] = 5.288
tasas["Hepatico"] = 5.18
tasas["Respiratorio"] = 5.12
tasas["Renal"] = 5.051
tasas["Neurologico"] = 5.188
tasas["Traumatologico"] = 5.094
tasas["Esofagico"] = 5.048
tasas["Oftalmologico"] = 5.168
tasas["Circulatorio"] = 5.237
tasas["Intestinal"] = 4.985


def generar_dia():
    llegadas_dia = []

    for grd in tasas:
        for i in range(poisson(tasas[grd])):
            llegadas_dia.append(grd)
    shuffle(llegadas_dia)
    return llegadas_dia


def generador_llegadas(n_simulaciones, dias_totales):

    set_de_colas_por_replica = []
    for replica in range(n_simulaciones):
        colas_por_dia = []
        for dia in range(dias_totales):

            cola = generar_dia()
            colas_por_dia.append(cola)

        set_de_colas_por_replica.append(colas_por_dia)

    return set_de_colas_por_replica


if __name__ == "__main__":

    n, dias = "a", "b"

    while not n.isdigit() and not dias.isdigit():
        n = input("Ingrese el número de Réplicas:\n>\t")
        dias = input("Ingrese el número de días:\n>\t")

    n = int(n)
    dias = int(dias)

    print("\nCreando colas..")
    colas = generador_llegadas(n, dias)
    print("\nColas creadas para {} simulaciones y {} días".format(n, dias))

    print("\nCreando Archivo..")
    with open(NOMBRE_ARCHIVO, "w") as outfile:

        json.dump(colas, outfile)

    print("\nContenido guardado en el archivo '{}'".format(NOMBRE_ARCHIVO))





