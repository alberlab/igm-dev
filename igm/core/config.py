"""
Copyright (C) 2017 University of Southern California and
                    Nan Hua, Guido Polles

This would be the core part of IGM. Defining the config class will be 
the common messager for all steps.

"""

from __future__ import division, print_function
import yaml
import os


from . import defaults

schema_file = os.path.join(
    os.path.dirname( os.path.abspath(defaults.__file__) ),
    'config_schema.yaml'
)
with open(schema_file) as y:
    schema = yaml.safe_load(y)


