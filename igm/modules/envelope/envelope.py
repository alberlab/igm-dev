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

class NuclearEnvelope(Restraint):
    """
    A object handles nuclear envelope restraints
    Parameters
    ----------
    cfg configure object
    """
    def __init__(self, cfg):
        self.type = module_name
        self.root = schema_root
        
        self.shape = unicode(cfg[self.root + "/envelope/nucleus_shape"])
        
        if self.shape == u"sphere":
            self.a = self.b = self.c = float(cfg[self.root + "/envelope/nucleus_axes"])
        elif self.shape == u"ellipsoid":
            self.a, self.b, self.c = cfg[self.root + "/envelope/nucleus_axes"]
        
        self.kspring = cfg[self.root + "/envelope/nucleus_kspring"]
    
    def Lammps(self, Lmp, **kwargs):
        normal = kwargs.pop("normal_group","NORMAL")
        
        Lmp.fix('Envelope0', normal, 'ellipsoidalenvelope', self.a, self.b, self.c, self.kspring)
        Lmp.fix_modify("Envelope0", 'energy', 'yes')
        
    def getScore(self, particles):
        return 0
    
    def getViolationRatio(self, particles):
        return 0