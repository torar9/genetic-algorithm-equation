from GeneticAlgorithm import GeneticAlgorithm
from Chromosome import Chromosome
from decimal import *

wantedResult = 38
population = 6
parentLen = 6
mutationRate = 3
mutationChance = 10

alg = GeneticAlgorithm(wantedResult, population, parentLen, mutationRate, mutationChance)
alg.generatePopulation()

result: Chromosome
generation = 0
while True:
    generation += 1
    print("Generation: ", generation)
    alg.calculateObjectiveValues()
    alg.calculateFitnessValues()

    alg.printChromosomes()
    print()
    alg.doRouleteWheel()
    # alg.printParents()

    alg.doCrossOverAndMutate()
    result = alg.checkIfFinished()
    if result is not None:
        break

print("%d + %d + %d = %d" %(result.a, result.b, result.c, wantedResult))

print("End")