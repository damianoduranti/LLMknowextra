import pathlib
import glob
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_json_data(file_path):
    """
    Reads and returns the content of a JSON file.

    Parameters:
    - file_path (str): Path to the JSON file to read.

    Returns:
    - dict: Parsed JSON data from the file.

    Raises:
    - FileNotFoundError: If the JSON file cannot be found.
    - json.JSONDecodeError: If there is an error parsing the JSON.
    """
    if not pathlib.Path(file_path).is_file():
        logging.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format: {file_path}")
        raise json.JSONDecodeError(f"Invalid JSON format: {file_path}")

def validate_json_structure(data):
    """
    Validate the structure of JSON data to ensure it contains necessary keys 'P' or 'N'.

    Parameters:
        data (dict): JSON data to validate.

    Returns:
        tuple: A boolean indicating validation success and a descriptive message.
    """
    required_keys = ['P', 'N']
    valid = any(key in data for key in required_keys if isinstance(data.get(key), list) and data[key])

    if not valid:
        message = "JSON data must include non-empty 'P' or 'N' lists."
        logging.error(message)
        return False, message

    if 'S' in data and (not isinstance(data['S'], list) or not all(isinstance(item, str) for item in data['S'])):
        message = "Invalid format for propositional letters in 'S'."
        logging.error(message)
        return False, message

    return True, "JSON structure is valid."

def generate_ltl_prompt(data):
    """
    Generates a prompt for LTL process mining based on provided trace data, including constraints on propositional letters if available.
    Adjusts the prompt based on the presence of positive, negative, or both traces, handles singular and plural cases,
    ensures continuous numbering across both sets of traces, and removes excessive spacing between traces of the same type.

    Parameters:
    - data (dict): Trace data containing 'P' for positive trace, 'N' for negative trace, and optionally 'S' for propositional letters constraints.

    Returns:
    - str: Generated prompt for LTL process mining on the given traces.
    """
    def traces_to_str(traces, start_index=1):
        """Converts trace data to a string format with labeled traces, ensuring continuous numbering and minimal spacing."""
        traces_str = ""
        trace_index = start_index
        for trace in traces:
            if trace_index > start_index:
                traces_str += "\n"
            traces_str += f"FINITE TRACE {trace_index}\n\n"
            for step_index, event in enumerate(trace, start=1):
                traces_str += f"{step_index}. {{ {', '.join(event)} }}\n"
            trace_index += 1

        return traces_str, trace_index

    positive_str = ""
    negative_str = ""
    constraint_info = ""

    trace_counter = 1
    if 'P' in data and data['P']:
        positive_str, trace_counter = traces_to_str(data['P'], trace_counter)
    if 'N' in data and data['N']:
        negative_str, _ = traces_to_str(data['N'], trace_counter)

    propositional_letters = sorted(set(data.get('S', [])))
    if propositional_letters:
        letters_str = ', '.join([f'"{letter}"' for letter in propositional_letters])
        letter_or_letters = "propositional letter" if len(propositional_letters) == 1 else "propositional letters"
        constraint_info = f", using only the {letter_or_letters} {letters_str}"
    else:
        constraint_info = ""

    if positive_str and negative_str:
        prompt = f"Provide an LTLf formula{constraint_info} that is satisfied on:\n\n{positive_str}\nand falsified on:\n\n{negative_str}\nProvide the formula only in the form of a string, using the nuXmv syntax."
    elif positive_str:
        prompt = f"Provide an LTLf formula{constraint_info} that is satisfied on:\n\n{positive_str}\nProvide the formula only in the form of a string, using the nuXmv syntax."
    elif negative_str:
        prompt = f"Provide an LTLf formula{constraint_info} that is falsified on:\n\n{negative_str}\nProvide the formula only in the form of a string, using the nuXmv syntax."
    else:
        return "No valid trace data provided."

    return prompt.strip()

def get_ltl_constraints(data):
    """
    Extracts propositional letters constraints from trace data.

    Parameters:
    - data (dict): Trace data containing 'S' for propositional letters constraints.

    Returns:
    - list: List of propositional letters constraints.
    """
    return sorted(set(data.get('S', [])))

def generate_ltl_prompts_from_json(file_path):
    """
    Generates an LTL process mining prompt from a JSON file, with added validation.

    Parameters:
    - file_path (str): Path to the JSON file.

    Returns:
    - str: Generated prompt, or None if an error occurs.
    """
    try:
        data = read_json_data(file_path)
        is_valid, validation_message = validate_json_structure(data)
        if not is_valid:
            logging.error(f"Validation failed for {file_path}: {validation_message}")
            return None
        return generate_ltl_prompt(data)
    except Exception as e:
        logging.error(f"Error generating prompt from {file_path}: {e}")
        return None

def generate_ltl_prompts_from_json_batch(directory_path):
    """
    Generates LTL process mining prompts from all JSON files within a specified directory,
    sorted alphabetically.

    Parameters:
    - directory_path (str): Directory containing JSON files.

    Returns:
    - list: List of generated prompts.
    """
    prompts = []
    for file_path in sorted(glob.glob(os.path.join(directory_path, '*.json'))):
        prompt = generate_ltl_prompts_from_json(file_path)
        if prompt:
            prompts.append(prompt)
        else:
            logging.info(f"Skipping file: {file_path}")
    return prompts

def generate_dl_prompt(data, ontology):
    """
    Generates a prompt for DL concept learning based on provided instance data and ontology.

    Parameters:
    - data (dict): Instance data containing 'instances' for concept instances.
    - ontology (str): OWL ontology content.

    Returns:
    - str: Generated prompt for DL concept learning on the given instances and ontology.
    """

    separation_type = data.get('separation')

    if separation_type == 'strong':
        positive_examples = "\n\n".join([f"K |= C({example})" for example in data['P']])
        negative_examples = "\n\n".join([f"K |= ¬C({example})" for example in data['N']])

        prompt = (f"Given the following knowledge base K:\n\n{ontology}\n\n"
                f"Provide an ALCO Description Logic concept C that strongly separates the positive examples: "
                f"E+ = {{{', '.join(data['P'])}}}, from the negative examples: E- = {{{', '.join(data['N'])}}}.\n\n"
                "This means that:\n\n"
                f"{positive_examples}\n\n"
                "whereas\n\n"
                f"{negative_examples}")    
        
    elif separation_type == 'weak':
        positive_examples = "\n\n".join([f"K |= C({example})" for example in data['P']])
        negative_examples = "\n\n".join([f"K \\not |= C({example})" for example in data['N']])

        prompt = (f"Given the following knowledge base K:\n\n{ontology}\n\n"
                f"Provide an ALCO Description Logic concept C that weakly separates the positive examples: "
                f"E+ = {{{', '.join(data['P'])}}}, from the negative examples: E- = {{{', '.join(data['N'])}}}.\n\n"
                "This means that:\n\n"
                f"{positive_examples}\n\n"
                "whereas\n\n"
                f"{negative_examples}")
    
    prompt += "\n\nProvide the concept using the Owlready2 syntax, in the form of: \n\nwith onto: \n\tclass C(...): \n\t\tequivalent_to = [...]. Do not include anything else in the response."
    
    return prompt.strip()

def generate_dl_prompts_from_json(file_path, ontology_path):
    """
    Generates a DL concept learning prompt from a JSON file, with added validation.

    Parameters:
    - file_path (str): Path to the JSON file.
    - ontology_path (str): Path to the OWL ontology file.

    Returns:
    - str: Generated prompt, or None if an error occurs.
    """
    try:
        data = read_json_data(file_path)
        ontology = ""
        with open(ontology_path, 'r') as file:
            ontology = file.read()
        return generate_dl_prompt(data, ontology)
    except Exception as e:
        logging.error(f"Error generating prompt from {file_path}: {e}")
        return None
    
def generate_dl_prompts_from_json_batch(directory_path, ontology_path):
    """
    Generates DL concept learning prompts from all JSON files within a specified directory,
    sorted alphabetically.

    Parameters:
    - directory_path (str): Directory containing JSON files.
    - ontology_path (str): Path to the OWL ontology file.

    Returns:
    - list: List of generated prompts.
    """
    prompts = []
    for file_path in sorted(glob.glob(os.path.join(directory_path, '*.json'))):
        prompt = generate_dl_prompts_from_json(file_path, ontology_path)
        if prompt:
            prompts.append(prompt)
        else:
            logging.info(f"Skipping file: {file_path}")
    return prompts