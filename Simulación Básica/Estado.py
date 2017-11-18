from PoliticasTransferencia import *
from set_politicas import *


def calcular_estado_sistema_transferencia(self):

    if self.disponibilidad_criticas <= 0.1:

        if self.disponibilidad_intermedias <= 0.4:

            return "E01"

        elif self.disponibilidad_intermedias <= 0.6:

            return "E02"


        elif self.disponibilidad_intermedias <= 0.85:

            return "E03"

        else:

            return "E04"


    elif self.disponibilidad_criticas <= 0.2:

        if self.disponibilidad_intermedias <= 0.4:

            return "E11"

        elif self.disponibilidad_intermedias <= 0.6:

            return "E12"


        elif self.disponibilidad_intermedias <= 0.85:

            return "E13"

        else:

            return "E14"

    else:
        if self.disponibilidad_intermedias <= 0.4:

            return "E21"

        elif self.disponibilidad_intermedias <= 0.6:

            return "E22"


        elif self.disponibilidad_intermedias <= 0.85:

            return "E23"

        else:

            return "E24"


def calcular_estado_recibir_intermedia(self, avanzados, deseados_esperados, deseados_arribados):
    if avanzados <= 30:
        if self.disponibilidad_intermedias <= 0.1:
            if deseados_esperados - deseados_arribados >= 6:
                return "E000"
            else:
                return "E001"
        elif self.disponibilidad_intermedias <= 0.2:
            if deseados_esperados - deseados_arribados >= 6:
                return "E010"
            else:
                return "E011"
        else:
            if deseados_esperados - deseados_arribados >= 6:
                return "E020"
            else:
                return "E021"
    else:
        if self.disponibilidad_intermedias <= 0.1:
            if deseados_esperados - deseados_arribados >= 6:
                return "E100"
            else:
                return "E101"
        elif self.disponibilidad_intermedias <= 0.2:
            if deseados_esperados - deseados_arribados >= 6:
                return "E110"
            else:
                return "E111"
        else:
            if deseados_esperados - deseados_arribados >= 6:
                return "E120"
            else:
                return "E121"





politicas_transferencia_hacia_intermedia = {"E{}{}".format(i, j): None for i in range(3) for j in range(1, 5)}


politicas_transferencia_hacia_intermedia["E04"] = bajar_todo_critica
politicas_transferencia_hacia_intermedia["E14"] = bajar_todo_critica
politicas_transferencia_hacia_intermedia["E24"] = bajar_todo_critica
politicas_transferencia_hacia_intermedia["E13"] = bajar_todo_critica
politicas_transferencia_hacia_intermedia["E23"] = bajar_todo_critica
politicas_transferencia_hacia_intermedia["E22"] = bajar_todo_critica


politicas_transferencia_hacia_intermedia["E03"] = bajar_con_reserva_moderada
politicas_transferencia_hacia_intermedia["E12"] = bajar_con_reserva_moderada
politicas_transferencia_hacia_intermedia["E21"] = bajar_con_reserva_moderada

politicas_transferencia_hacia_intermedia["E01"] = bajar_con_reserva_agresiva
politicas_transferencia_hacia_intermedia["E02"] = bajar_con_reserva_agresiva
politicas_transferencia_hacia_intermedia["E11"] = bajar_con_reserva_agresiva


politicas_llegadas_intermedias = {"E{}{}{}".format(i, j, k): None for i in range(2) for j in range(3) for k in range(2)}

politicas_llegadas_intermedias["E000"] = recibir_deseados_intermedia
politicas_llegadas_intermedias["E001"] = recibir_deseados_intermedia
politicas_llegadas_intermedias["E110"] = recibir_deseados_intermedia
politicas_llegadas_intermedias["E010"] = recibir_deseados_intermedia
politicas_llegadas_intermedias["E100"] = recibir_deseados_intermedia

politicas_llegadas_intermedias["E111"] = recibir_todo_intermedia
politicas_llegadas_intermedias["E011"] = recibir_todo_intermedia
politicas_llegadas_intermedias["E120"] = recibir_todo_intermedia
politicas_llegadas_intermedias["E121"] = recibir_todo_intermedia
politicas_llegadas_intermedias["E021"] = recibir_todo_intermedia
politicas_llegadas_intermedias["E101"] = recibir_todo_intermedia
politicas_llegadas_intermedias["E020"] = recibir_todo_intermedia


if __name__ == "__main__":
    print(politicas_transferencia_hacia_intermedia)