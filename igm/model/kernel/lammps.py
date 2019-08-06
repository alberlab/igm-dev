from __future__ import print_function, division
from lammps import PyLammps
import numpy as np
import os
class LammpsKernel(IGMKernel):
    def __init__(self, model, cfg, runid):
        self.cfg = cfg
        self.model = model
        self.runid = runid
        
        self.tmp_dir = self.cfg.tmpdir('optimization')
        self.randseed = int(self.cfg["optimization/kernel_opts/lammps/seed"])
        
        self.initLammps()
        
        self.setupSimulationBox()
        
        self.setupParticles()
        self.setCoordinates()
        self.setRadii()
        
        self.setupNeighbor()
        
    def initLammps(self):
        """
        setup lammps python interface, log file
        """
        if self.cfg["optimization/kernel_opts/lammps/keep_logs"]:
            self.Lmp = PyLammps(cmdargs=["-log",os.path.join(self.tmp_dir, self.runid+".log")])
        else:
            self.Lmp = PyLammps(cmdargs=["-log","none"])
        self.Lmp.atom_style("bond")
        self.Lmp.boundary('s','s','s')
    
    def setupSimulationBox(self):
        """
        setup lammps simulation box
        """
        atom_types = 1
        bond_types = 0
        bond_per_atom = 0
        for Res in self.model.restraints:
            atom_types += Res.extra_atom_types
            bond_types += Res.extra_bond_types
            bond_per_atom += Res.extra_bond_per_atom
            
            if res.type == "Envelope":
                xx , yy, zz = Res.a*1.2, Res.b*1.2, Res.c*1.2
        
        self.Lmp.region("IGMBOX", "block", -xx, xx, -yy, yy, -zz, zz)
        self.Lmp.create_box(1, "IGMBOX", "bond/types", bond_types, "extra/bond/per/atom", bond_per_atom)
    
    def setupParticles(self):
        """
        initialize particles with random position
        """
        
        #add user define per-atom property: radius(double)
        self.Lmp.fix("UserProperty","all","property/atom","d_radius")
        
        #number of particles
        self.nbead = len(self.model.particles)
        
        self.atom_style_index = 1
        self.Lmp.create_atoms(1, "random", self.nbead, self.randseed, "IGMBOX")
        
        #set particle mass 1.0
        self.Lmp.mass('*', 1.0)
        
        #group particle NORMAL
        self.lmp_group_NORMAL = "NORMAL"
        self.Lmp.group(self.lmp_group_NORMAL, "type", 1)
        
        #get numpy view of per atom array
        
        self.particle_id  = self.Lmp.lmp.numpy.extract_atom_iarray('id', n, 1)
        self._coordinates = self.Lmp.lmp.numpy.extract_atom_darray('x', n, 3)
        self._radii       = self.lmp.lmp.numpy.extract_atom_darray('d_radius', n, 1)
        
    def indexMapping(self):
        """
        particle mapping from lammps index to original index
        """
        return np.argsort( self.particle_id[:, 0] )
    
    def setCoordinates(self, crd = None):
        """
        assign xyz values to lammps
        """
        if crd:
            self.coordinates[self.indexMapping(), :] = crd[:]
        else:
            self.coordinates[self.indexMapping(), :] = self.model.particles.coordinates[:]
        
    def setRadii(self, radii = None):
        """
        assign radius values to lammps
        """
        if radii:
            self.radii[self.indexMapping(), :]       = radii[:]
        else:
            self.radii[self.indexMapping(), :]       = self.model.particles.radii[:]
            
        self.maxrad = max(self.radii)
        
    def setupNeighbor(self):
        """
        setup neighbor list rules
        """
        if hasattr(self, "maxrad"):
            self.Lmp.neighbor(self.maxrad, 'bin')
        else:
            raise RuntimeError("Radii not set before setupNeighbor()")
            
        max_neighbor = int(self.cfg["optimization/kernel_opts/lammps/max_neigh"])
        
        self.Lmp.neigh_modify('every',1,'check','yes')
        self.Lmp.neigh_modify("one", max_neighbor, 'page', 20*max_neighbor)
    
    def addRestraints(self):
        """
        add restraints to lammps one by one
        """
        #lammps bond style definition
        bond_styles = set()
        n = 1
        for Res in self.model.restraints:
            if hasattr(Res, "bond_style"):
                bond_styles.add(Res.bond_style)
                
                #give_bond_id
                Res.setBondId(n)
                n += 1
        if len(bond_styles) == 1:
            self.Lmp.bond_style(bond_styles.pop())
        elif len(bond_styles) > 1:
            cmd = ["bond_style", "hybrid"]
            while bond_styles:
                cmd.append(bond_styles.pop())
            self.Lmp.command(" ".join(cmd))
            
        #define variable for fast communication/avoid input string parsing
        self.Lmp.variable("batoms","string","EMPTY")
        bond_variable = "batoms"
        
        #loop all restraints and apply lammps code
        for Res in self.model.restraints:
            Res.Lammps(self.Lmp, runid         = self.runid, 
                                 tmp_dir       = self.tmp_dir, 
                                 randseed      = self.randseed, 
                                 normal_group  = self.lmp_group_NORMAL,
                                 bond_variable = bond_variable)
    
    
def optimize(model, cfg):
    
    
