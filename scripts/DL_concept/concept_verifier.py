import logging
from owlready2 import get_ontology, sync_reasoner, Thing, Not

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_ontology(ontology_path):
    """
    Load an OWL ontology from a specified file path.
    
    Parameters:
        ontology_path (str): Path to the OWL ontology file.
    
    Returns:
        Ontology: The loaded ontology object.
    """
    try:
        ontology = get_ontology(f"file://{ontology_path}").load()
        logging.info(f"Ontology loaded successfully from {ontology_path}")
        return ontology
    except Exception as e:
        logging.error(f"Failed to load ontology: {e}")
        raise

def create_names_mapping(ontology):
    """
    Creates mappings for classes, properties, and individuals in an ontology.
    
    Parameters:
        ontology (Ontology): The ontology to map.
    
    Returns:
        tuple: Mappings for classes, properties, and individuals.
    """
    class_mapping = {cls.name.split('.')[-1]: cls for cls in ontology.classes()}
    properties_mapping = {prop.name.split('.')[-1]: prop for prop in ontology.properties()}
    individuals_mapping = {ind.name.split('.')[-1]: ind for ind in ontology.individuals()}
    return class_mapping, properties_mapping, individuals_mapping

def assign_dynamic_variables(mapping):
    """
    Dynamically assign variables in the global scope based on the provided mapping.
    """
    globals().update(mapping)

def clean_dynamic_variables(mapping):
    """
    Clean up dynamically assigned variables from the global scope.
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
    relevant_mappings = {k: v for k, v in {**class_mapping, **properties_mapping, **individuals_mapping}.items() if k in response}
    assign_dynamic_variables(relevant_mappings)

    try:
        with ontology:
            class C(Thing):
                equivalent_to = [eval(response)]
            sync_reasoner()

        if separation_type == 'weak':
            return list(ontology.get_instances_of(C))
        
        else:
            with ontology:
                class NotC(Thing):
                    equivalent_to = [Not(eval(response))]
                sync_reasoner()
            return list(ontology.get_instances_of(C)), list(ontology.get_instances_of(NotC))
    except Exception as e:
        logging.error(f"Failed to evaluate or reason over response: {e}")
        raise
    finally:
        clean_dynamic_variables(relevant_mappings)

def main():
    print(concept_verifier(load_ontology('data/DL_concept/1/1_ontology.owl'), """
    with onto:
        class C(Thing):
                equivalent_to = [Student & (studiesAt.some(EuUni))]""", separation_type='weak'))

if __name__ == '__main__':
    main()