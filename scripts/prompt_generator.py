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

def generate_ltl_prompt(data):
    """
    Generates a prompt for an LTL formula based on provided trace data, including constraints on propositional letters if available.
    Unpacks letters singularly, bracketing them and correctly handling singular and plural cases.

    Parameters:
    - data (dict): Trace data containing 'P' for positive trace, 'N' for negative trace, and optionally 'S' for propositional letters constraints.

    Returns:
    - str: Generated prompt for the LTL formula.
    """
    def trace_to_str(trace):
        """Converts trace data to a string format."""
        return '\n'.join(f"{i + 1}. {{ {', '.join(sorted(set(event)))} }}" for i, event in enumerate(trace))

    positive_str = trace_to_str(data.get('P', [[]])[0])
    negative_str = trace_to_str(data.get('N', [[]])[0])
    
    # Extract propositional letters if provided and format them
    propositional_letters = sorted(set(data.get('S', [])))
    letters_str = ', '.join([f'"{letter}"' for letter in propositional_letters])  # Bracket each letter individually

    # Handle singular and plural cases
    letter_or_letters = "letter" if len(propositional_letters) == 1 else "letters"
    
    constraint_info = ""
    if propositional_letters:
        constraint_info = f", using only the propositional {letter_or_letters} {letters_str}"
    
    return (f"Provide an LTL formula{constraint_info} that is satisfied on the following trace:\n\n{positive_str}\n\n"
            f"and falsified on the following trace:\n\n{negative_str}")

def generate_prompts_from_json(file_path):
    """
    Generates an LTL formula prompt from a JSON file.

    Parameters:
    - file_path (str): Path to the JSON file.

    Returns:
    - str: Generated prompt, or None if an error occurs.
    """
    try:
        data = read_json_data(file_path)
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