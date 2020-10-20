

class Formulas(object):
    primeira_iteracao = True
    alpha = 1
    beta = 5
    a = 0.01  # taxa de evaporacao do feromonio
    Q = 20  # constante de atualizacao de feromonio

    mat_dist = [[0, 22, 50, 48, 29],
                [22, 0, 30, 34, 32],
                [50, 30, 0, 22, 23],
                [48, 34, 22, 0, 35],
                [29, 32, 23, 35, 0]]

    mat_ferom = [[0, 0.1, 0.1, 0.1, 0.1],
                 [0.1, 0, 0.1, 0.1, 0.1],
                 [0.1, 0.1, 0, 0.1, 0.1],
                 [0.1, 0.1, 0.1, 0, 0.1],
                 [0.1, 0.1, 0.1, 0.1, 0]]

    @staticmethod
    def inverso_distancia(origem, destino):
        return 1 / Formulas.mat_dist[origem][destino]

    @staticmethod
    def evaporacao(origem, destino):
        return -(1 - Formulas.a) * Formulas.mat_ferom[origem][destino]

    @staticmethod
    def inv_dist_x_feromonio(origem, destino):
        return (Formulas.mat_ferom[origem][destino] ** Formulas.alpha) * (Formulas.inverso_distancia(origem, destino) ** Formulas.beta)

    @staticmethod
    def probabilidade(origem, destino):
        numerador = Formulas.inv_dist_x_feromonio(origem, destino)
        denominador = 0
        for i in range(5):
            if i == origem:
                continue
            denominador += Formulas.inv_dist_x_feromonio(origem, i)
        return numerador / denominador

    @staticmethod
    def atualiza_feromonio(formigas):
        if Formulas.primeira_iteracao is False:
            for i in range(len(formigas)):
                for j in range(len(formigas)):
                    if j == i:
                        continue

                    for k in range(len(formigas)):
                        if [i, j] in formigas[k].cam_perc:
                            Formulas.mat_ferom[i][j] += Formulas.Q / formigas[k].dist_total
                        else:
                            continue
                    Formulas.mat_ferom[i][j] += Formulas.evaporacao(i, j)