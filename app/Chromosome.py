from decimal import *

class Chromosome:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.objValue = Decimal(0)
        self.fitValue = Decimal(0)
        self.propability = Decimal(0)
        self.propStart = Decimal(0)
        self.propEnd = Decimal(0)

    def getBits(self):
        return "{0:b}".format(self.a).zfill(8) + "{0:b}".format(self.b).zfill(8) + "{0:b}".format(self.c).zfill(8)