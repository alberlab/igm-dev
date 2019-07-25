from __future__ import division, absolute_import, print_function
import numpy as np

class Restraint(object):
    """
    Define Basic restarint type
    """
    
    
    def __init__(self, rtype, particles, para, note=''):
        self.rtype      = rtype
        self.particles  = particles
        self.parameters = para
        self.note       = note
        
    
    def getScore(self):
        return 0
        
    def getViolationRatio(self):
        return 0
        

class ExcludedVolume(Restraint):
    rtype_id = 0
    rtype_repr = "EXCLUDED_VOLUME"
    
    def __init__(self, pid, k=1.0, note=''):
        self.pid  = pid
        self.k    = k
        self.note = note
       
        self.rnum = len(particles)*(len(particles)-1)/2
    
    def __str__(self):
        return "Restraint: {} (Particles: {}) {}".format(self.rtype_repr,
                                                         len(self.particles),
                                                         self.note)
    
    def getScore(self, particlesi):
        return self.getScore(particles).sum()
        
    def getScores(self, particles):
        from scipy.spatial import distance
        crd = particles.getCoordinates()
        rad = particles.getRadii()
        
        dist = distance.pdist(crd)
        cap  = distance.pdist(rad, lambda u, v: u+v)
        s    = (cap - dist).clip(min=0)
        
        return s.ravel()