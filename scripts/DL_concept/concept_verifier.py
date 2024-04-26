import logging
import json
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
    response = response.replace('onto.', '')
    return response[1:]

def concept_verifier(instances, ontology, response):
    """
    Verify a DL concept based on a given response.

    Parameters:
    - instances (str): str containing instances and separation type for the concept.
    - ontology (owlready2.namespace.Ontology): The ontology to use for verification.
    - response (str): The response from the LLM.

    Returns:
    - list: Instances of the verified concept.
    """
    separation_type = instances.get('separation')
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
            instances = list(ontology.get_instances_of(C))
            return [instance.name.split('.')[-1] for instance in instances], []
        
        else:
            with ontology:
                class NotC(Thing):
                    equivalent_to = [Not(eval(response))]
                sync_reasoner()
            instances, not_instances = list(ontology.get_instances_of(C)), list(ontology.get_instances_of(NotC))
            return [instance.name.split('.')[-1] for instance in instances], [instance.name.split('.')[-1] for instance in not_instances]
    except Exception as e:
        logging.error(f"Failed to evaluate or reason over response: {e}")
        raise
    finally:
        clean_dynamic_variables(relevant_mappings)

def evaluator(instances, verified_response):
    """
    Evaluate the instances of a verified concept based on the separation type.

    Parameters:
    - instances (str): str containing instances and separation type for the concept.
    - verified_response (tuple): Tuple containing the entailed instances of the concept 
        (and for strong separation also the entailed instances of the negation of the concept).

    Returns:
    - bool: True if candidate evaluation is successful, False otherwise.
    - error: Error message if candidate evaluation fails.
    """
    separation_type = instances.get('separation')
    positive_examples = instances['P']
    negative_examples = instances['N']

    error = None

    if all(example in verified_response[0] for example in positive_examples):
        if separation_type == 'strong':
            if all(example in verified_response[1] for example in negative_examples):
                logging.info("Candidate evaluation successful.")
                return True, error
            else:
                error = ("Candidate evaluation failed [sep_type=strong - some negative examples not entailed].")
                return False, error
        else:
            if not any(example in verified_response[0] for example in negative_examples):
                logging.info("Candidate evaluation successful.")
                return True, error
            else:
                error = ("Candidate evaluation failed [sep_type=weak - some negative examples entailed].")
                return False, error
    else:
        error = (f"Candidate evaluation failed [some positive examples not entailed].")
        return False, error

def main():
    verified_response = (concept_verifier(json.load(open('data/DL_concept/strong_sep/1/1_instances.json')),load_ontology('data/DL_concept/strong_sep/1/1_ontology.owl'), """
    with onto:
        class C(Thing):
                equivalent_to = [Student & (studiesAt.some(EuUni))]"""))
    
    print(f"Verified instances: {(verified_response)}")
    evaluator(json.load(open('data/DL_concept/strong_sep/1/1_instances.json')), verified_response)

if __name__ == '__main__':
    main()