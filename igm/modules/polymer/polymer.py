from __future__ import division, print_function
from ..restraint import Restraint
import yaml
import os

def _load_schema(yamlFilename="defaults.yaml"):

    schema_file = os.path.join(
        os.path.dirname( os.path.abspath(__file__) ),
        yamlFilename
    )
    with open(schema_file) as y:
        schema_dict = yaml.safe_load(y)
    
    return schema_dict


_schema_dict = _load_schema()

module_name = _schema_dict["Module"]

schema_root = _schema_dict["Root"]
schema = _schema_dict["Defaults"]

class Polymer(Restraint):
    """
    Object handles consecutive bead restraint
    Parameters
    ----------
    cfg: configure object
    index : alabtools.index object
        chromosome chain index
    """
    def __init__(self, cfg, index):
        self.type = module_name
        self.root = schema_root
        
        self.contact_range = float(cfg[self.root + "/polymer/contact_range"])
        self.style         = cfg[self.root + "/polymer/polymer_bonds_style"]
        self.kspring       = float(cfg[self.root + "/polymer/polymer_kspring"])
        
        self.bead_i = []
        self.bead_j = []
        if self.style == "none":
            pass
        if self.style == "simple":
            self.bond_style = "soft_contact"
            for i in range(len(index) - 1):
                if (index.chrom[i] == index.chrom[i+1] and
                    index.copy[i] == index.copy[i+1]):
                    
                    self.bead_i.append(i)
                    self.bead_j.append(i+1)
                    
        elif self.style == "hic":
            raise NotImplementedError()
            
    def setBondId(self, bid):
        self.bid = bid
        
    @property
    def extra_bond_types(self):
        return 1    
    @property
    def extra_bond_per_atom(self):
        return 2
        
    def Lammps(self, Lmp, **kwargs):
        try:
            # python 2 izip
            from itertools import izip as zip
        except ImportError: 
            pass
            
        bond_variable = kwargs.pop("bond_variable", None)
        if bond_variable is None:
            raise RuntimeError("No bond variable is set!")
        
        Lmp.bond_coeff(self.bid, "soft_contact", self.kspring, self.contact_range) #kspring, contact_range
        bonds = []
        for i, j in zip(self.bead_i, self.bead_j):
            bonds.append("{}:{}".format(i+1, j+1))
            
        Lmp.lmp.set_variable(bond_variable,' '.join(bonds)) #avoid input command parsing


        Lmp.add_multiple_bonds( self.bid, "variable", bond_variable )
        
        Lmp.lmp.set_variable(bond_variable, "EMPTY") # reset variable
        
    def getScore(self, particles):
        return 0
    
    def getViolationRatio(self, particles):
        return 0