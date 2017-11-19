from PoliticasTransferencia import *
from set_politicas import *


def calcular_estado_sistema_transferencia(disponibilidad_criticas, disponibilidad_intermedias):

    if disponibilidad_criticas <= 10:

        if disponibilidad_intermedias <= 20:

            return "E01"
        elif disponibilidad_intermedias <= 40:

            return "E02"

        elif disponibilidad_intermedias <= 80:

            return "E03"
        else:

            return "E04"

    elif disponibilidad_criticas <= 20:

        if disponibilidad_intermedias <= 20:

            return "E11"

        elif disponibilidad_intermedias <= 40:

            return "E12"


        elif disponibilidad_intermedias <= 80:

            return "E13"

        else:

            return "E14"

    else:
        if disponibilidad_intermedias <= 20:

            return "E21"

        elif disponibilidad_intermedias <= 40:

            return "E22"


        elif disponibilidad_intermedias <= 80:
            return "E23"

        else:
            return "E24"


def calcular_estado_recibir_critica(disponibilidad_criticas, avanzados, deseados_esperados, deseados_arribados):
    if avanzados <= 25:
        if disponibilidad_criticas <= 35:
            if deseados_esperados - deseados_arribados >= 17:
                return "E000"
            else:
                return "E001"
        elif disponibilidad_criticas <= 70:
            if deseados_esperados - deseados_arribados >= 17:
                return "E010"
            else:
                return "E011"
        else:
            if deseados_esperados - deseados_arribados >= 17:
                return "E020"
            else:
                return "E021"
    else:
        if disponibilidad_criticas <= 35:
            if deseados_esperados - deseados_arribados >= 17:
                return "E100"
            else:
                return "E101"
        elif disponibilidad_criticas <= 70:
            if deseados_esperados - deseados_arribados >= 17:
                return "E110"
            else:
                return "E111"
        else:
            if deseados_esperados - deseados_arribados >= 17:
                return "E120"
            else:
                return "E121"


def calcular_estado_recibir_intermedia(disponibilidad_intermedias, avanzados, deseados_esperados, deseados_arribados):
    if avanzados <= 25:
        if disponibilidad_intermedias <= 10:
            if deseados_esperados - deseados_arribados >= 7:
                return "E000"
            else:
                return "E001"
        elif disponibilidad_intermedias <= 20:
            if deseados_esperados - deseados_arribados >= 7:
                return "E010"
            else:
                return "E011"
        else:
            if deseados_esperados - deseados_arribados >= 7:
                return "E020"
            else:
                return "E021"
    else:
        if disponibilidad_intermedias <= 10:
            if deseados_esperados - deseados_arribados >= 7:
                return "E100"
            else:
                return "E101"
        elif disponibilidad_intermedias <= 20:
            if deseados_esperados - deseados_arribados >= 7:
                return "E110"
            else:
                return "E111"
        else:
            if deseados_esperados - deseados_arribados >= 7:
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



respuesta_gestor_transferencia = {"E{}{}".format(i, j): None for i in range(3) for j in range(1, 5)}


respuesta_gestor_transferencia["E04"] = (False, 0, "Bajar los {} posibles")
respuesta_gestor_transferencia["E14"] = (False, 0, "Bajar los {} posibles")
respuesta_gestor_transferencia["E24"] = (False, 0, "Bajar los {} posibles")
respuesta_gestor_transferencia["E13"] = (False, 0, "Bajar los {} posibles")
respuesta_gestor_transferencia["E23"] = (False, 0, "Bajar los {} posibles")
respuesta_gestor_transferencia["E22"] = (False, 0, "Bajar los {} posibles")


respuesta_gestor_transferencia["E03"] = (True, -1, "Bajar {} Pacientes")
respuesta_gestor_transferencia["E12"] = (True, -1, "Bajar {} Pacientes")
respuesta_gestor_transferencia["E21"] = (True, -1, "Bajar {} Pacientes")

respuesta_gestor_transferencia["E01"] = (True, 1, "Bajar {} Pacientes")
respuesta_gestor_transferencia["E02"] = (True, 1, "Bajar {} Pacientes")
respuesta_gestor_transferencia["E11"] = (True, 1, "Bajar {} Pacientes")



politicas_llegadas_criticas = {"E{}{}{}".format(i, j, k): None for i in range(2) for j in range(3) for k in range(2)}

politicas_llegadas_criticas["E000"] = recibir_priorizado_criticas
politicas_llegadas_criticas["E001"] = recibir_priorizado_criticas
politicas_llegadas_criticas["E110"] = recibir_priorizado_criticas
politicas_llegadas_criticas["E010"] = recibir_priorizado_criticas
politicas_llegadas_criticas["E100"] = recibir_priorizado_criticas

politicas_llegadas_criticas["E111"] = recibir_todo_critica
politicas_llegadas_criticas["E011"] = recibir_todo_critica
politicas_llegadas_criticas["E120"] = recibir_todo_critica
politicas_llegadas_criticas["E121"] = recibir_todo_critica
politicas_llegadas_criticas["E021"] = recibir_todo_critica
politicas_llegadas_criticas["E101"] = recibir_todo_critica
politicas_llegadas_criticas["E020"] = recibir_todo_critica

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


respuesta_gestor_recibir_c = {"E{}{}{}".format(i, j, k): None for i in range(2) for j in range(3) for k in range(2)}

respuesta_gestor_recibir_c["E000"] = (True, "Recibir pacientes: {}")
respuesta_gestor_recibir_c["E001"] = (True, "Recibir pacientes: {}")
respuesta_gestor_recibir_c["E110"] = (True, "Recibir pacientes: {}")
respuesta_gestor_recibir_c["E010"] = (True, "Recibir pacientes: {}")
respuesta_gestor_recibir_c["E100"] = (True, "Recibir pacientes: {}")

respuesta_gestor_recibir_c["E111"] = (False, "Recibir cualquier paciente Crítico")
respuesta_gestor_recibir_c["E011"] = (False, "Recibir cualquier paciente Crítico")
respuesta_gestor_recibir_c["E120"] = (False, "Recibir cualquier paciente Crítico")
respuesta_gestor_recibir_c["E121"] = (False, "Recibir cualquier paciente Crítico")
respuesta_gestor_recibir_c["E021"] = (False, "Recibir cualquier paciente Crítico")
respuesta_gestor_recibir_c["E101"] = (False, "Recibir cualquier paciente Crítico")
respuesta_gestor_recibir_c["E020"] = (False, "Recibir cualquier paciente Crítico")

respuesta_gestor_recibir_i = {"E{}{}{}".format(i, j, k): None for i in range(2) for j in range(3) for k in range(2)}

respuesta_gestor_recibir_i["E000"] = "Recibe: Oftalmológico, Esofágico"
respuesta_gestor_recibir_i["E001"] = "Recibe: Oftalmológico, Esofágico"
respuesta_gestor_recibir_i["E110"] = "Recibe: Oftalmológico, Esofágico"
respuesta_gestor_recibir_i["E010"] = "Recibe: Oftalmológico, Esofágico"
respuesta_gestor_recibir_i["E100"] = "Recibe: Oftalmológico, Esofágico"

respuesta_gestor_recibir_i["E111"] = "Recibe: Oftalmológico, Esofágico, Intestinal"
respuesta_gestor_recibir_i["E011"] = "Recibe: Oftalmológico, Esofágico, Intestinal"
respuesta_gestor_recibir_i["E120"] = "Recibe: Oftalmológico, Esofágico, Intestinal"
respuesta_gestor_recibir_i["E121"] = "Recibe: Oftalmológico, Esofágico, Intestinal"
respuesta_gestor_recibir_i["E021"] = "Recibe: Oftalmológico, Esofágico, Intestinal"
respuesta_gestor_recibir_i["E101"] = "Recibe: Oftalmológico, Esofágico, Intestinal"
respuesta_gestor_recibir_i["E020"] = "Recibe: Oftalmológico, Esofágico, Intestinal"


if __name__ == "__main__":
    print(politicas_transferencia_hacia_intermedia)