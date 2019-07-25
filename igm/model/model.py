from __future__ import division, absolute_import, print_function
import numpy as np
from .particle import Particles
try:
    from itertools import izip as zip
except ImportError: 
    pass

class Model(object):
    """
    
    Modeling target system
    
    This is an abstract mid-layer between data-restraints and minization kernel.
    
    The Model holds all information about the target system by particles and
    restraints.
    
    """
    
    def __init__(self, uid=0):
         
        self.particles = Particles()
        
        self.restraints = []
        self.id = uid
    
    
    def initParticles(self, crd, rad):
        self.particles.initParticles(crd, rad)
        
    def addParticle(self, pos, r, t=0):
        self.particles.append(pos, r, t)
    
    def getCoordinates(self):
        return self.particles.getCoordinates()
    def getRadii(self):
        return self.particles.getRadii()
    #====restraint methods
    def addRestraint(self, res, override=False):
        """
        Add a type of restraint to model
        """
        res._apply_model(self, override)
        
        res._apply(self)
    
    def evalRestraint(self, i):
        """
        get force score
        """
        
        return self.restraints[i].getScore(self.particles)
    
    def evalRestraintViolationRatio(self, i):
        """
        get force violation ratio
        """
        
        return self.restraints[i].getViolationRatio(self.particles)
    #====
    def optimize(self, cfg):
        """
        optimize the model by selected kernel
        """
        
        if cfg['optimization']["kernel"] == "lammps":
            from .kernel import lammps
            return lammps.optimize(self, cfg)
        #-
    #-
    
    def saveCoordinates(self, filename):
        """
        save xyz coordinates into numpy npy file
        """
        
        np.save(filename, self.getCoordinates())
    #-
    
    def saveXYZR(self, filename):
        """
        save xyzr into numpy npz file
        """
        
        np.savez(filename, xyz=self.getCoordinates(), r=self.getRadii())
    #-
        
#=