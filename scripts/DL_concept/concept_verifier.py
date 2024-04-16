import os
import subprocess
import resource
import logging
from owlready2 import *

def load_ontology(ontology_path):
    """
    Load the specified OWL ontology file.

    Parameters:
    - ontology_path (str): Path to the OWL ontology file to load.

    Returns:
    - owlready2.namespace.Ontology: The loaded ontology.
    """
    return get_ontology(f"file://{ontology_path}").load()

def create_names_mapping(ontology):
    """
    Create a mapping of class names to their corresponding OWL classes.

    Parameters:
    - ontology (owlready2.namespace.Ontology): The ontology to create the mapping from.

    Returns:
    - dict: Mapping of class names to owlready2.entity.ThingClass objects.
    """
    class_mapping = {}
    properties_mapping = {}
    individuals_mapping = {}

    for cls in ontology.classes():
        base_name = cls.name.split('.')[-1]
        class_mapping[base_name] = cls

    for prop in ontology.properties():
        base_name = prop.name.split('.')[-1]
        properties_mapping[base_name] = prop

    for inst in ontology.individuals():
        base_name = inst.name.split('.')[-1]
        individuals_mapping[base_name] = inst

    return class_mapping, properties_mapping, individuals_mapping

def assign_dynamic_variables(mapping):
    """
    Assign dynamic variables based on the provided mapping.
    """
    for key, value in mapping.items():
        globals()[key] = value
    
def clean_dynamic_variables(mapping):
    """
    Clean dynamic variables based on the provided mapping.
    """
    for key in mapping.keys():
        globals().pop(key, None)

def clean_response(response):
    """
    Clean the response and mantain only what is inside square brackets.

    Parameters:
    - response (str): The response to clean.

    Returns:
    - str: The cleaned response.
    """
    response = response[response.find('['):response.rfind(']')]
    return response[1:]

def concept_verifier(ontology, response, separation_type='strong'):
    """
    Verify a DL concept based on a given response.

    Parameters:
    - ontology (owlready2.namespace.Ontology): The ontology to use for verification.
    - response (str): The response to verify.

    Returns:
    - list: Instances of the verified concept.
    """
    response = clean_response(response)

    class_mapping, properties_mapping, individuals_mapping = create_names_mapping(ontology)

    keys = list(class_mapping.keys())
    class_match = []
    for key in keys:
        if key in response:
            class_match.append(key)

    keys = list(properties_mapping.keys())
    property_match = []
    for key in keys:
        if key in response:
            property_match.append(key)

    keys = list(individuals_mapping.keys())
    individual_match = []
    for key in keys:
        if key in response:
            individual_match.append(key)

    assign_dynamic_variables({k: class_mapping[k] for k in class_mapping if k in response})
    assign_dynamic_variables({k: properties_mapping[k] for k in properties_mapping if k in response})
    assign_dynamic_variables({k: individuals_mapping[k] for k in individuals_mapping if k in response})

    with ontology:
        class C(Thing):
            equivalent_to = [eval(response)]
        sync_reasoner()

    if separation_type == 'weak':
        clean_dynamic_variables(class_mapping)
        clean_dynamic_variables(properties_mapping)
        clean_dynamic_variables(individuals_mapping)
        return list(ontology.get_instances_of(C))
    
    else:
        with ontology:
            class NotC(Thing):
                equivalent_to = [Not(eval(response))]
            sync_reasoner()

        clean_dynamic_variables(class_mapping)
        clean_dynamic_variables(properties_mapping)
        clean_dynamic_variables(individuals_mapping)
        return list(ontology.get_instances_of(C)), list(ontology.get_instances_of(NotC))

def main():
    print(concept_verifier(load_ontology('data/DL_concept/1/1_ontology.owl'), """
    with onto:
        class C(Thing):
                equivalent_to = [Student & (studiesAt.some(EuUni))]""", separation_type='weak'))

if __name__ == '__main__':
    main()