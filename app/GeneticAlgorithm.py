import random as rnd
import math
from decimal import Decimal
from Chromosome import Chromosome

class GeneticAlgorithm():
    def __init__(self, wantedResult: int, population: int, parentLen: int, mutationRate: float):
        self.wantedResult = abs(wantedResult)
        self.population = population
        self.parentLen = parentLen
        self.matePos = 1
        self.mutationRate = mutationRate
        self.id = 0
        self.chromosomes = []
        self.parents = []

    def generatePopulation(self):
        for i in range(self.population):
            self.chromosomes.append(
                Chromosome(
                    rnd.randint(0, 255),
                    rnd.randint(0, 255),
                    rnd.randint(0, 255)))

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
        self.parents = []
        for _ in range(self.parentLen):
            x = Decimal(rnd.uniform(0, 1))
            for n in self.chromosomes:
                if x >= n.propStart and x < n.propEnd:
                    self.parents.append(n)

    def doCrossOverAndMutate(self):
        for _ in range(2):
            for i in range(int(self.parentLen / 2)):
                mom: Chromosome = self.parents[i]
                dad: Chromosome = self.parents[i + 1]

                momChrom: str = mom.getBits()
                dadChrom: str = dad.getBits()

                crossPos = rnd.randint(1, 24)

                child = ""
                for x in range(24):
                    if x < crossPos:
                        child += momChrom[x]
                    else:
                        child += dadChrom[x]

                chance = rnd.uniform(0, 1)
                if chance < self.mutationRate:
                    for _ in range(math.ceil(24 * self.mutationRate)):
                        pos = rnd.randint(0, 24 - 1)
                        new = child[pos]

                        if new == "1":
                            new = "0"
                        else:
                            new = "1"

                        child = child[:pos] + new + child[pos + 1:]

                childChrom = Chromosome(int(child[:8], 2), int(child[8:16], 2), int(child[16:24], 2))
                self.chromosomes.append(childChrom)
                self.chromosomes.pop(0)

    def checkIfFinished(self) -> Chromosome:
        for e in self.chromosomes:
            if (e.a + e.b + e.c) == self.wantedResult:
                return e
        return None

    def getChromosomesString(self):
        result = ""
        for e in self.chromosomes:
            result += ("a: %03d b: %03d c: %03d obj: %3d fitt: %.3f prop: %.3f propStart: %.3f propEnd: %.3f \n" %(e.a, e.b, e.c, e.objValue, e.fitValue, e.propability, e.propStart, e.propEnd))
        return result
