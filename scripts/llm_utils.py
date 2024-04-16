import os
import openai
import logging
import json

# Initialize logging with a specific format for timestamps, log level, and messages.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_api_keys(file_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'api_keys.json')):
    """
    Loads all API keys from a specified JSON file and sets them as environment variables.
    
    Parameters:
    - file_path (str): Path to the JSON file containing the API keys.
    
    Raises:
    - FileNotFoundError: Raised if the specified file_path does not exist.
    - json.JSONDecodeError: Raised if the file is not a valid JSON document.
    """
    try:
        with open(file_path, 'r') as file:
            api_keys = json.load(file)
            for key, value in api_keys.items():
                os.environ[key.upper()] = value
        logging.info("API keys loaded successfully.")
    except FileNotFoundError:
        logging.error(f"API keys file not found: {file_path}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from file: {file_path}")
        raise

def validate_environment_variables(required_env_vars):
    """
    Validates that all required environment variables are set.
    
    Parameters:
    - required_env_vars (list): A list of strings representing the keys of required environment variables.
    
    Returns:
    - bool: True if all required environment variables are set, otherwise False.
    """
    missing_vars = [var for var in required_env_vars if var not in os.environ]
    if missing_vars:
        logging.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    return True

def set_openai_api_configurations():
    """
    Sets OpenAI API configurations using values from environment variables.
    
    Returns:
    - bool: True if configurations are successfully applied, otherwise False.
    """
    required_env_vars = ['OPENAI_API_KEY', 'OPENAI_DEPLOYMENT_NAME', 'OPENAI_API_BASE', 'OPENAI_API_TYPE', 'OPENAI_API_VERSION']
    if not validate_environment_variables(required_env_vars):
        logging.error("OpenAI API configurations are incomplete. Please check your environment variables.")
        return False
    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.api_base = os.environ['OPENAI_API_BASE']
    openai.api_type = os.environ['OPENAI_API_TYPE']
    openai.api_version = os.environ['OPENAI_API_VERSION']
    return True

def send_prompt(prompt):
    """
    Sends a specified prompt to the OpenAI API for completion and retrieves the response.
    
    Parameters:
    - prompt (str): The text prompt to send to the OpenAI API.
    
    Returns:
    - str: The text content of the response from the API, or None if an error occurs.
    """
    phrase = [{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
            engine=os.environ['OPENAI_DEPLOYMENT_NAME'],
            messages=phrase,
            max_tokens=200,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logging.error(f"Failed to send prompt to API: {e}")
        return None