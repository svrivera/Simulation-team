import math


class GRD:
    def __init__(self, nombre, tasa):
        self.tasa = tasa
        self.diccionario = {}
        self.lista = []
        self.name = nombre

    def calculo_probabilidad(self, x):
        prob = math.exp(-self.tasa) * self.tasa ** x / math.factorial(x)
        self.diccionario[x] = prob

    def elegir_porcentaje(self, porcentaje, max):
        actual = 0
        i = 0
        while actual <= porcentaje:
            abajo = int(self.tasa)-i
            arriba = int(self.tasa)+i
            if i == 0:
                actual += self.diccionario[int(self.tasa)]
                self.lista.append(int(self.tasa))
            elif abajo < 0 and arriba <= max:
                actual += self.diccionario[arriba]
                self.lista.append(arriba)
            elif abajo >= 0 and arriba > max:
                actual += self.diccionario[abajo]
                self.lista.append(abajo)

            elif abajo < 0 and arriba > max:
                break

            else:
                lista = sorted([(abajo, self.diccionario[abajo]),
                                (arriba, self.diccionario[arriba])], key= lambda x: x[1])

                actual += lista[-1][1]
                self.lista.append(lista[-1][0])
                if actual < porcentaje:
                    actual += lista[0][1]
                    self.lista.append(lista[0][0])
            i += 1




#Parametros"
max = 30
porcentaje = 0.95












GRD_Coronario = GRD("Coronario", tasa=5.288)
GRD_Hepatico = GRD("Hepatico", tasa=5.188)
GRD_Respiratorio = GRD("Respiratorio", tasa=5.12)
GRD_Renal = GRD("Renal", tasa=5.051)
GRD_Neurologico = GRD("Neurologico", tasa=5.188)
GRD_Traumatologico = GRD("Traumatologico", tasa=5.094)
GRD_Esofagico = GRD("Esofagico", tasa=5.048)
GRD_Oftalmologico = GRD("Oftalmologico", tasa=5.168)
GRD_Circulatorio = GRD("Circulatorio", tasa=5.237)
GRD_Intestinal = GRD("Intestinal", tasa=4.985)

lista_grds = [GRD_Coronario, GRD_Hepatico, GRD_Respiratorio, GRD_Renal, GRD_Neurologico, GRD_Traumatologico,
              GRD_Esofagico, GRD_Oftalmologico, GRD_Circulatorio, GRD_Intestinal]

for i in range(max +1):
    for grd in lista_grds:
        grd.calculo_probabilidad(i)

for grd in lista_grds:
    grd.elegir_porcentaje(porcentaje, max)


with open("Calculo_probabilidades.txt", 'w') as file:
    for grd in lista_grds:
        contador = 0
        print(grd.name, "\n")
        file.write(grd.name + '\n')
        for key in sorted(grd.lista):
            print("Cantidad de Pacientes: {},    Probabilidad: {} \n".format(key, grd.diccionario[key]))
            file.write("Cantidad de Pacientes: {},    Probabilidad: {} \n".format(key, grd.diccionario[key]))
            contador += grd.diccionario[key]
        file.write("Total: {} \n".format(contador))
        print("Total: {} \n".format(contador))
        file.write('\n')
        print('\n')
