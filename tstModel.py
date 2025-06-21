from model.model import Model

mymodel = Model()
mymodel.buildGraph(1951)
nodi, archi = mymodel.getGraphDetails()
print("Num nodi", nodi, "Num archi", archi)
