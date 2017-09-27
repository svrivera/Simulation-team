from Hospital import Simulacion




for i in range(1):
    s = Simulacion(tiempo_simulacion = 30,
                 n_criticas = 18,
                 n_intermedias = 30,
                 n_basicas = 30)
    s.run()

