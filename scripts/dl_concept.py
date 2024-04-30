import logging
import os
import json
import time
import csv
import re
from prompt_generator import generate_dl_prompts_from_json
from llm_utils import send_prompt, load_api_keys, set_openai_api_configurations
from DL_concept.concept_verifier import evaluator, concept_verifier, load_ontology

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_output_dir(trace_path, folder_name):
    parts = trace_path.split('/')
    constraint_type = parts[2]
    
    output_dir = os.path.join("output", "DL_concept", constraint_type, folder_name)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def dl_concept(instances_path, ontology_path, max_attempts=5):
    """
    Generate DL candidates until a correct DL concept is found.

    Parameters:
        instances_path (str): Path to the JSON instances file.
        ontology_path (str): Path to the OWL ontology file.
        max_attempts (int): Maximum number of attempts to find a valid DL concept.

    Returns:
        response(str): A correct DL concept if found, None otherwise.
        int: The number of attempts made until a correct concept is found.
    """
    try:
        results_dir = create_output_dir(instances_path, "results")
        load_api_keys(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'api_keys.json'))
        set_openai_api_configurations()
        durations = []

        for attempt in range(1, max_attempts + 1):
            start_time = time.time()
            
            try:
                prompt = generate_dl_prompts_from_json(instances_path, ontology_path)
                response = str(send_prompt(prompt)).strip()

                logging.info(f"Attempt {attempt} response: {response}")

                instances = json.load(open(instances_path))
                ontology = load_ontology(ontology_path)

                verified_response = concept_verifier(instances, ontology, response)
                
                logging.info(f"Attempt {attempt} verified response: {verified_response}")

                if verified_response:
                    result, error = evaluator(instances, verified_response)

                else:
                    result = False
                    error = "Error verifying the candidate concept." 

            except Exception as e:
                logging.error(f"Error in attempt {attempt}: {e}")
                result = False
                error = f"Error in attempt {attempt}: {e}"

            durations.append(time.time() - start_time)

            result_path = os.path.join(results_dir, f"result_{attempt}.txt")
            with open(result_path, 'w') as f:
                f.write(f"Prompt: {prompt}\nResponse: {response}\nVerified Response: {verified_response}\nError: {error}\nResult: {result}\n")
                logging.info(f"Attempt {attempt} results saved to: {result_path}")
            if result:
                return response, durations
            time.sleep(1)
    except Exception as e:
        logging.error(f"An error occurred during processing: {e}")
    return None, durations

def main():

    with open("dl_times.csv", 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Separation Type', 'Trace', 'Duration', "Result"])

        for separation_type in os.listdir("data/DL_concept"):
            if separation_type == ".DS_Store":
                continue
            for trace in sorted(os.listdir(f"data/DL_concept/{separation_type}")):
                if trace == ".DS_Store":
                    continue
                trace_path = os.path.join("data/DL_concept", separation_type, trace)
                instances_path = os.path.join(trace_path, f"{trace}_instances.json")
                ontology_path = os.path.join(trace_path, f"{trace}_ontology.owl")
                response, durations = dl_concept(instances_path, ontology_path)
                writer.writerow([separation_type, trace, durations, 'Correct' if response else 'Incorrect'])

if __name__ == "__main__":
    main()