import yaml
import os

def _load_schema():

    schema_file = os.path.join(
        os.path.dirname( os.path.abspath(__file__) ),
        'config_schema.yaml'
    )
    with open(schema_file) as y:
        schema = yaml.safe_load(y)
    
    return schema
    
schema = _load_schema()
