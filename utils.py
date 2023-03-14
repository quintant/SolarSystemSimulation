

from math import cos, log, pi
from random import lognormvariate, normalvariate, random

from numpy import sign


def rad(mass, norm=False):
    # return log(pi * pow(mass, 2))
    if norm:
        return max(log(mass),1)
    else:
        return log(mass)
    # return mass /100

def massDist(mu=1, sigma=.5):
    return lognormvariate(mu=mu, sigma=sigma)

def posDist(mu, sigma=600, p=10, pf=cos):
    # return normalvariate(mu, sigma=sigma)
    n = normalvariate(300, sigma=sigma) * pf(p)
    return n + mu