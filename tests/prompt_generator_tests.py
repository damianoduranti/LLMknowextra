import logging
from scripts.prompt_generator import *

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_tests():
    """
    Runs example test cases demonstrating the functionality with improved print formatting.
    """
    logging.info("Starting tests...")

    # Test with a single JSON file
    example_file_path = 'data/LTL_unconstrained/1.json'
    print("Testing with a single JSON file:")
    print(f"File: {example_file_path}")
    try:
        prompt = generate_prompts_from_json(example_file_path)
        print(f"Prompt:\n{prompt}\n")
        print("-" * 50)  # Divider for readability
    except Exception as e:
        logging.error(f"Test with single file failed: {e}")
        print("-" * 50)  # Divider for readability

    # Test with a batch of JSON files
    directory_path = 'data/LTL_unconstrained/'
    print("Testing with a batch of JSON files:")
    print(f"Directory: {directory_path}")
    try:
        prompts = generate_prompts_from_json_batch(directory_path)
        for i, prompt in enumerate(prompts, start=1):
            #print file name
            print(f"Prompt {i}:\n{prompt}\n")
            print("-" * 50)  # Divider for readability
    except Exception as e:
        logging.error(f"Test with batch files failed: {e}")

if __name__ == "__main__":
    run_tests()
