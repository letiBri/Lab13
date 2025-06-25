import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapDriver = {}
        for d in DAO.getAllDrivers():
            self._idMapDriver[d.driverId] = d

        self._bestDreamTeam = []
        self._bestTasso = 100000

    def getYears(self):
        return DAO.getYears()

    def buildGraph(self, anno):
        self._graph.clear()

        nodes = DAO.getNodes(anno, self._idMapDriver)
        self._graph.add_nodes_from(nodes)

        for n1 in nodes:
            for n2 in nodes:
                peso = DAO.getPeso(anno, n1, n2)[0]
                if peso != 0:
                    self._graph.add_edge(n1, n2, weight=peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getBestDriver(self):
        bestDriver = (None, 0)
        degree_nodes = {}
        for n in self._graph.nodes():
            vittorie = 0
            for node in self._graph.successors(n):
                if self._graph.has_edge(n, node):
                    vittorie += self._graph[n][node]["weight"]
                if self._graph.has_edge(node, n):
                    vittorie -= self._graph[node][n]["weight"]
            degree_nodes[n] = vittorie
        for key, value in degree_nodes.items():
            # print(key, value)
            if value > bestDriver[1]:
                bestDriver = (key, value)
        return bestDriver

    # def getBestDriver(self):  # soluzione prof
    #     best = 0
    #     bestdriver = None
    #     for n in self._graph.nodes:
    #         score = 0
    #         for e_out in self._graph.out_edges(n, data=True):
    #             score += e_out[2]["weight"]
    #         for e_in in self._graph.in_edges(n, data=True):
    #             score -= e_in[2]["weight"]
    #
    #         if score > best:
    #             bestdriver = n
    #             best = score
    #
    #     print(f"Best driver: {bestdriver}, with score {best}")
    #     return bestdriver, best

    def getDreamTeam(self, k):
        self._bestDreamTeam = []
        self._bestTasso = 100000  # metto un valore alto perchè io voglio trovare il minimo
        parziale = []
        rimanenti = list(self._graph.nodes)
        self._ricorsione(k, parziale, rimanenti)
        return self._bestDreamTeam, self._bestTasso

    def _ricorsione(self, k, parziale, rimanenti):
        if len(parziale) == k:
            if self.getTasso(parziale) < self._bestTasso:
                self._bestTasso = self.getTasso(parziale)
                self._bestDreamTeam = copy.deepcopy(parziale)
        else:
            for n in rimanenti:
                parziale.append(n)
                rimanenti.remove(n)
                self._ricorsione(k, parziale, rimanenti)
                parziale.pop()
                rimanenti.append(n)

    def getTasso(self, parziale):
        if len(parziale) == 0:
            return 100000
        tassoTot = 0
        for p in parziale:
            sconfitte = 0
            predecessori = self._graph.predecessors(p)  # guardo solo gli archi entranti
            for pred in predecessori:
                if pred not in parziale:
                    sconfitte += self._graph[pred][p]["weight"]
            tassoTot += sconfitte
        # print(tassoTot)
        return tassoTot




