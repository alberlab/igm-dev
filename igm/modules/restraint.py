from __future__ import division, print_function


class Restraint(object):
    """
    Restraint object, takes care of data and translate to forces in model.
    Also keep track of forces added and can evaluate
    """
    def __init__(self):
        self.type = ""
    def __repr__(self):
        return self.type
    
    def __len__(self):
        raise(NotImplementedError())
        
    def __getitem__(self, key):
        raise(NotImplementedError())
        
    @property
    def extra_atom_types(self):
        return 0
    @property
    def extra_bond_types(self):
        return 0    
    @property
    def extra_bond_per_atom(self):
        return 0
    
    def getScore(self, particles):
        raise(NotImplementedError())
    
    def getViolationRatio(self, particles):
        raise(NotImplementedError())
        
    def _apply_model(self, model, override=False):
        """
        Attach restraint to model
        """
        if hasattr(self.model):
            if override:
                self.model = model
                self.model.restraints[self.index] = self
            else:
                raise(RuntimeError("Restraint alreay applyed to model! Set override to true to proceed."))
        except AttributeError:
            self.model = model
            self.model.restraints.append(self)
            self.index = len(self.model.restraints)
            
    def _apply(self, model, override=False):
        self._apply_model(model, override)
        
    