import logging
import time
import os
import re
from LTL_process.translator.formula_translator import f2i
from LTL_process.config import NUXMV
from LTL_process.smv_generator import generate_smv_files_from_json, generate_smv_spec
from LTL_process.formula_verifier import evaluator
from llm_utils import load_api_keys, set_openai_api_configurations, send_prompt
from prompt_generator import generate_ltl_prompts_from_json, read_json_data, validate_json_structure, get_ltl_constraints

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_output_dir(trace_path, folder_name):
    parts = trace_path.split('/')
    constraint_type = parts[2]
    file_id = os.path.splitext(parts[3])[0] 

    output_dir = os.path.join("output", "LTL_process", constraint_type, file_id, folder_name)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def ltl_process(trace_path, nuxmv_path=NUXMV, max_attempts=5):
    """
    Generate LTL candidates until a correct LTL process formula is found.

    Parameters:
        trace_path (str): Path to the JSON trace file.
        nuxmv_path (str): Path to the NuSMV executable.
        max_attempts (int): Maximum number of attempts to find a valid LTL formula through the LLM.

    Returns:
        str: A correct LTL process formula if found, None otherwise.
        int: The number of attempts made until a correct formula is found.
    """
    validate_json_structure(read_json_data(trace_path))
    traces_smv_dir = create_output_dir(trace_path, "traces_smv")
    generate_smv_files_from_json(trace_path, traces_smv_dir)

    results_dir = create_output_dir(trace_path, "results")

    load_api_keys(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'api_keys.json'))
    set_openai_api_configurations()

    for attempt in range(1, max_attempts + 1):
        try:
            prompt = generate_ltl_prompts_from_json(trace_path)
            response = str(send_prompt(prompt))
            response = re.sub(r'\"', '', response)

            logging.info(f"Attempt {attempt} response: {response}")

            syntax_error = None

            try:
                f2i_response = f2i(response)
            except Exception as e:
                logging.error(f"Syntax error in the candidate formula: {e}")
                f2i_response = None
                syntax_error = "The candidate formula contains a syntax error."

            logging.info(f"Attempt {attempt} f2i: {f2i_response}")

            if f2i_response:
                spec_dir = create_output_dir(trace_path, "spec")
                spec_path = generate_smv_spec(f2i_response, spec_dir)

                constraints = get_ltl_constraints(read_json_data(trace_path))
                if constraints:
                    lower = [char for char in response if char.islower()]
                    if not all(char in constraints for char in lower):
                        syntax_error = "The generated LTL formula does not satisfy the signature restrictions."

                result, error = evaluator(traces_smv_dir, spec_path)

                if syntax_error is not None:
                    error += syntax_error
                    result = False

            else:
                result = False
                error = syntax_error
        
        except Exception as e:
            logging.error(f"Error processing LTL formula: {e}")
            result = False
            response = None
            f2i_response = None
            spec_path = None

        result_path = os.path.join(results_dir, f"attempt_{attempt}.txt")
        with open(result_path, 'w') as file:
            file.write(f"Attempt: {attempt}\nPrompt: {prompt}\nResponse: {response}\nF2I Response: {f2i_response}\nError: {error}\nSpec Path: {spec_path}\nEvaluated Result: {result}\n")
            logging.info(f"Attempt {attempt} results saved to: {result_path}")
        if result:
            return response, attempt
        if attempt < max_attempts:
            time.sleep(10)

if __name__ == "__main__":
    ltl_process("data/LTL_process/constrained/7.1.json")