from __future__ import division, absolute_import, print_function
import numpy as np

    
class Particles(object):
    POSDTYPE = np.float32
    PTDTYPE = np.int8
    NORMAL = 0
    DUMMY_STATIC = 1
    DUMMY_DYNAMIC = 2
    PTYPES = ["NORMAL","DUMMY_STATIC","DUMMY_DYNAMIC"]
    def __init__(self):
        self.coordinates = np.empty((0, 3), dtype=self.POSDTYPE)
        self.radii       = np.empty((0, 1), dtype=self.POSDTYPE)
        self.ptypes      = np.empty(0, dtype=self.PTDTYPE)
        self.n           = 0
    
    def __str__(self):
        return "(Particles):{}".format(self.n)
    __repr__ = __str__
    
    def __len__(self):
        return self.n
    #====Particle methods
    def append(self, pos, r, type=0):
        """
        Add particle to system
        """
        
        self.coordinates = np.concatenate((self.coordinates, [np.array(pos)]), axis=0)
        self.radii       = np.concatenate((self.radii, [[r]]), axis=0)
        self.ptypes      = np.concatenate((self.ptypes, [type]))
        self.n           = len(self.coordinates)
        return self.n-1
        
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.getParticle(key)
            
    def getParticle(self,i):
        """
        Get particle in the system
        """
        if 0<=i<self.n:
            return (self.coordinates[i], self.radii[i], self.ptypes[i])
        else:
            return None
            
    def setParticle(self, i, pos=None, r=None, type=None):
        """
        set particle coordinates
        """
        if i<=0<self.n:
            if pos:
                self.coordinates[i] = np.array(pos, dtype=self.POSDTYPE)
            if r:
                self.radii[i] = r
            if type:
                self.ptype[i] = type
        else:
            raise(RuntimeError, "{} out of boundary {}".format(i, self.n))
    #====
    
    
    #===bulk particle methods
    def initParticles(self, crd, rad):
        """
        initialize particles using numpy array
        
        Parameters
        ----------
        crd : 2D numpy array (float), N*3
            Numpy array of coordinates for each particle, N is the number of particles
        rad : 2D numpy array (float), N*1
            particle radius
        """
        assert len(crd) == len(rad)
        assert len(crd[0]) == 3
        self.particles = np.array(crd, dtype=self.POSDTYPE)
        self.radii = np.array(rad, dtype=self.POSDTYPE)
        self.n = len(self.particles)
        self.ptype = np.zeros(self.n, dtype=self.PTDTYPE)
    #====
    
    
    #====bulk get methods
    def getCoordinates(self):
        """
        Get all particles' Coordinates in numpy array form
        """
        return self.particles[self.ptype == self.NORMAL]
    
    
    def getRadii(self):
        """
        Get all particles' radii in numpy array vector form
        """
        return np.array([self.radii[self.ptype == self.NORMAL]]).T
    #====     
