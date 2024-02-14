import logging
from scripts.prompt_generator import *
from scripts.llm_communicator import *

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generation_tests():
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
    #generation_tests()
    # Load API keys and set configurations
    load_api_keys()
    set_openai_api_configurations()

    # Example test: sending a custom prompt
    # Replace 'data/LTL_unconstrained/1.json' with the correct path or use another prompt generation method
    prompt = generate_prompts_from_json('data/LTL_unconstrained/1.json')
    print(f"Prompt: {prompt}")
    response = send_prompt(prompt)
    print(f"Response: {response}")



