import yaml
from typing import Any, Dict


def load_to_instance(file_name: str, instance: Any):
    loaded_data = yaml.safe_load(open(file_name))
    for attribute, value in dict(loaded_data).items():
        setattr(instance, attribute, value)
    return instance
