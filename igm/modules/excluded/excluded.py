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

class ExcludedVolume(Restraint):
    """
    ExculdedVolume Restraint object
    """
    def __init__(self, cfg):
        self.type = module_name
        self.root = schema_root
        
        self.evfactor = float(cfg[self.root + "/excluded/evfactor"])
    
    def Lammps(self, Lmp, **kwargs):
        Lmp.pair_style("excludedvolume", self.evfactor)
        Lmp.pair_coeff('*', '*', self.evfactor)
        
    def getScore(self, particles):
        return 0
    
    def getViolationRatio(self, particles):
        return 0
        