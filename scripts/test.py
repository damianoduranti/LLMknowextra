from scripts.llm_utils import *
from prompt_generator import *
from scripts.smv_generator import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Generate prompts from JSON files in the 'prompts' directory
json_path = "data/traces_json/LTL_unconstrained/1.json"
prompt = generate_prompts_from_json(json_path)
logging.info(f"Generated prompt: {prompt}")

# Create smv files from json
# Create an output directory for the SMV files here
output_directory = "data/test_files"
generate_smv_files_from_json(json_path, output_directory)

# Send prompt to the LLM
# COMMENTED OUT FOR NOT WASTING API CALLS
#load_api_keys()
#set_openai_api_configurations()
#logging.info(f"Sending prompt to the LLM: {prompt}")
#logging.info(f"Response: {send_prompt(prompt)}")