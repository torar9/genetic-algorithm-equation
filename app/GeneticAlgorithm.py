import random as rnd
from decimal import *
from Chromosome import Chromosome

class GeneticAlgorithm():
    chromosomes = []
    parents = []

    def __init__(self, wantedResult: int, population: int, parentLen: int, mutationRate: int, mutationChance: int):
        self.wantedResult = wantedResult
        self.population = population
        self.parentLen = parentLen
        self.matePos = 1
        self.mutationRate = mutationRate
        self.mutationChance = mutationChance

    def generatePopulation(self):
        for i in range(self.population):
            self.chromosomes.append(Chromosome(rnd.randint(0, 100), rnd.randint(0, 100), rnd.randint(0, 100)))

    def calculateObjectiveValues(self):
        for e in self.chromosomes:
            e.objValue = abs((e.a + e.b + e.c) - self.wantedResult)

    def calculateFitnessValues(self):
        total = Decimal(0)
        for e in self.chromosomes:
            e.fitValue = Decimal(1) / Decimal((Decimal(1) + e.objValue))
            total += e.fitValue

        sum = Decimal(0)
        for e in self.chromosomes:
            e.propStart = sum
            e.propability = Decimal(e.fitValue / total)
            sum += e.propability
            e.propEnd = sum

    def doRouleteWheel(self):
        for _ in range(self.parentLen):
            x = Decimal(rnd.uniform(0, 1))
            for n in self.chromosomes:
                if x >= n.propStart and x < n.propEnd:
                    self.parents.append(n)

    def doCrossOverAndMutate(self):
        pos = 0
        for i in range(int(self.parentLen / 2)):
            mom: Chromosome = self.parents[i]
            dad: Chromosome = self.parents[i + 1]

            momChrom: str = mom.getBits()
            dadChrom: str = dad.getBits()

            tmpM = momChrom[23:]
            tmpD = dadChrom[23:]
            momChrom = momChrom[:23] + tmpD
            dadChrom = dadChrom[:23] + tmpM

            for _ in range(self.mutationRate):
                x = rnd.randint(1, 100)
                if x <= self.mutationChance:
                    pos = rnd.randint(0, 24)
                    momChrom = momChrom[:pos - 1] + str(rnd.randint(0, 1)) + momChrom[pos:]
                    dadChrom = dadChrom[:pos - 1] + str(rnd.randint(0, 1)) + dadChrom[pos:]
            pos += 2;

            mom.a = int(momChrom[:8], 2)
            dad.a = int(dadChrom[:8], 2)
            mom.b = int(momChrom[8:16], 2)
            dad.b = int(dadChrom[8:16], 2)
            mom.c = int(momChrom[16:24], 2)
            dad.c = int(dadChrom[16:24], 2)

            self.parents[i] = dad
            self.parents[i + 1] = mom

    def checkIfFinished(self) -> Chromosome:
        for e in self.chromosomes:
            if (e.a + e.b + e.c) == self.wantedResult:
                return e
        return None

    def printChromosomes(self):
        for e in self.chromosomes:
            print("a: %3d b: %3d c: %3d obj: %3d fitt: %f prop: %f propStart: %f propEnd: %f" %(e.a, e.b, e.c, e.objValue, e.fitValue, e.propability, e.propStart, e.propEnd))