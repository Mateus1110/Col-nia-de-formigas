from Colonia_formigas.formulas import Formulas
from copy import deepcopy, copy
from random import uniform


class Ant(object):
    count_formigas = 1
    cidades_iniciais = [['A', 0], ['B', 1], ['C', 2], ['D', 3], ['E', 4]]
    cont = 0

    def __init__(self):
        self.id = Ant.count_formigas
        self.cidade_origem = Ant.cidades_iniciais[Ant.cont]

        self.possiveis_caminhos = self.set_caminhos()

        self.pos_atual = self.cidade_origem
        self.dist_total = 0

        self.cidades_visitadas = []
        self.cidades_visitadas.append(self.cidade_origem)
        self.cam_perc = []
        self.vet_prob = []
        Ant.count_formigas += 1
        Ant.cont += 1

    @staticmethod
    def cria_formigas(formigas):
        for i in range(5):
            obj = Ant()
            formigas.append(obj)

    def set_caminhos(self):
        list_aux = deepcopy(Ant.cidades_iniciais)
        list_aux.remove(self.cidade_origem)
        return list_aux

    def caminha(self):

        if len(self.possiveis_caminhos) == 0:
            self.dist_total += Formulas.mat_dist[self.pos_atual[1]][self.cidade_origem[1]]
            self.cam_perc.append([self.pos_atual[1], self.cidade_origem[1]])
            self.pos_atual = copy(self.cidade_origem)
            return

        self.vet_prob = []
        for destino in Ant.cidades_iniciais:
            if destino not in self.possiveis_caminhos or self.pos_atual[1] == destino[1]:
                self.vet_prob.append(0)
                continue
            else:
                self.vet_prob.append(Formulas.probabilidade(self.pos_atual[1], destino[1]))

        indice = Ant.roleta(self.vet_prob)
        aux = Ant.cidades_iniciais[indice]

        if aux not in self.cidades_visitadas:
            self.cidades_visitadas.append(aux)

        self.possiveis_caminhos.remove(aux)
        self.dist_total += Formulas.mat_dist[self.pos_atual[1]][aux[1]]

        self.cam_perc.append([self.pos_atual[1], aux[1]])
        self.pos_atual = copy(aux)

    @staticmethod
    def reseta_formigas(formigas):
        for obj in formigas:
            obj.cam_perc = []
            obj.cidades_visitadas = []
            obj.dist_total = 0
            obj.possiveis_caminhos = obj.set_caminhos()

    @staticmethod
    def roleta(vet_prob):
        aux_vet_prob = sorted(vet_prob, reverse=True)
        rand = uniform(0, sum(vet_prob))
        soma = 0
        valor = aux_vet_prob[-1]

        for i in range(5):
            if rand <= aux_vet_prob[i] + soma:
                valor = aux_vet_prob[i]
                break
            else:
                soma += aux_vet_prob[i]
        indice = vet_prob.index(valor)
        return indice

    @staticmethod
    def ant_system(formigas):
        iteracoes = 100
        etapas = 5
        for k in range(iteracoes):
            for obj in formigas:
                obj.caminha()
            etapas -= 1
            Formulas.atualiza_feromonio(formigas)
            Formulas.primeira_iteracao = False

            if etapas == 0:
                if k < iteracoes:
                    Ant.print_formigas(formigas, k + 1)
                    Ant.reseta_formigas(formigas)
                    etapas = 5

    @staticmethod
    def print_formigas(formigas, k):
        print('\033[33m{}ª iteracao:\033[m'.format(k // 5))
        for obj in formigas:
            print('formiga {} andou {}'.format(obj.id, obj.dist_total))

        for obj in formigas:
            print('formiga {},'
                  ' cidade origem: {},'
                  ' cidades visitadas: {}, '
                  'caminho percorrido: {}'
                  ''.format(obj.id, obj.cidade_origem, str(obj.cidades_visitadas), str(obj.cam_perc)))
        print('\n')