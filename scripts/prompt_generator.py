import glob
import json
import os
import logging

# Setup basic logging configuration
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
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format: {file_path}")
        raise

def validate_json_structure(data):
    """
    Validates the structure of the input JSON data, ensuring at least one of 'P' or 'N' is present and non-empty.

    Parameters:
    - data (dict): The JSON data to validate.

    Returns:
    - (bool, str): A tuple of a boolean indicating whether the data is valid and string message with result.
    """
    required_keys = ['P', 'N']
    valid_data_found = False  # Flag to track if valid 'P' or 'N' data is found

    for key in required_keys:
        if key in data:
            if not isinstance(data[key], list):
                return False, f"Expected a list for key: {key}"
            if len(data[key]) > 0:
                # Check for valid trace structure
                for trace in data[key]:
                    if not isinstance(trace, list):
                        return False, f"Expected a list of traces for key: {key}"
                    for event in trace:
                        if not isinstance(event, list):
                            return False, f"Expected a list of events in traces for key: {key}"
                valid_data_found = True  # Valid 'P' or 'N' data found

    if not valid_data_found:
        return False, "Both 'P' and 'N' are missing or empty. At least one must be present and non-empty."

    # Validate 'S' if present
    if 'S' in data and (not isinstance(data['S'], list) or any(not isinstance(letter, str) for letter in data['S'])):
        return False, "Invalid format for propositional letters in 'S'"
    
    return True, "JSON structure is valid."

def generate_ltl_prompt(data):
    """
    Generates a prompt for an LTL formula based on provided trace data, including constraints on propositional letters if available.
    Adjusts the prompt based on the presence of positive, negative, or both traces, handles singular and plural cases,
    ensures continuous numbering across both sets of traces, and removes excessive spacing between traces of the same type.

    Parameters:
    - data (dict): Trace data containing 'P' for positive trace, 'N' for negative trace, and optionally 'S' for propositional letters constraints.

    Returns:
    - str: Generated prompt for the LTL formula.
    """
    def traces_to_str(traces, start_index=1):
        """Converts trace data to a string format with labeled traces, ensuring continuous numbering and minimal spacing."""
        traces_str = ""
        trace_index = start_index
        for trace in traces:
            if trace_index > start_index:  # Add a single newline before subsequent traces, if not the first one
                traces_str += "\n"
            traces_str += f"TRACE {trace_index}\n\n"
            for step_index, event in enumerate(trace, start=1):
                traces_str += f"{step_index}. {{ {', '.join(event)} }}\n"
            trace_index += 1

        return traces_str, trace_index

    positive_str = ""
    negative_str = ""
    constraint_info = ""

    trace_counter = 1  # Start trace numbering
    if 'P' in data and data['P']:
        positive_str, trace_counter = traces_to_str(data['P'], trace_counter)
    if 'N' in data and data['N']:
        negative_str, _ = traces_to_str(data['N'], trace_counter)  # Continue numbering for negative traces

    propositional_letters = sorted(set(data.get('S', [])))
    if propositional_letters:
        letters_str = ', '.join([f'"{letter}"' for letter in propositional_letters])
        letter_or_letters = "propositional letter" if len(propositional_letters) == 1 else "propositional letters"
        constraint_info = f", using only the {letter_or_letters} {letters_str}"
    else:
        constraint_info = ""

    prompt_parts = []
    if positive_str and negative_str:
        prompt = f"Provide an LTL formula{constraint_info} that is satisfied on:\n\n{positive_str}\nand falsified on:\n\n{negative_str}"
    elif positive_str:
        prompt = f"Provide an LTL formula{constraint_info} that is satisfied on:\n\n{positive_str}"
    elif negative_str:
        prompt = f"Provide an LTL formula{constraint_info} that is falsified on:\n\n{negative_str}"
    else:
        return "No valid trace data provided."

    return prompt.strip()

def generate_prompts_from_json(file_path):
    """
    Generates an LTL formula prompt from a JSON file, with added validation.

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

def generate_prompts_from_json_batch(directory_path):
    """
    Generates LTL formula prompts from all JSON files within a specified directory,
    sorted alphabetically.

    Parameters:
    - directory_path (str): Directory containing JSON files.

    Returns:
    - list: List of generated prompts.
    """
    prompts = []
    # Sort the file paths alphabetically
    for file_path in sorted(glob.glob(os.path.join(directory_path, '*.json'))):
        prompt = generate_prompts_from_json(file_path)
        if prompt:
            prompts.append(prompt)
        else:
            logging.info(f"Skipping file: {file_path}")
    return prompts