import os
import openai
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_api_keys(file_path=None):
    """
    Load API keys from a JSON file and set them as environment variables.

    Parameters:
        file_path (str): Path to the JSON file containing the API keys.

    Raises:
        FileNotFoundError: If the file_path does not exist.
        json.JSONDecodeError: If the file is not a valid JSON document.
    """
    if file_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'config', 'api_keys.json')

    try:
        with open(file_path, 'r') as file:
            api_keys = json.load(file)
        for key, value in api_keys.items():
            os.environ[key.upper()] = value
        logging.info("API keys loaded successfully.")
    except FileNotFoundError:
        logging.error(f"API keys file not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from file: {file_path}")
        raise

def validate_environment_variables(required_env_vars):
    """
    Validate that all required environment variables are set.

    Parameters:
        required_env_vars (list): Keys of required environment variables.

    Returns:
        bool: True if all required environment variables are set, False otherwise.
    """
    missing_vars = [var for var in required_env_vars if var not in os.environ]
    if missing_vars:
        logging.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    return True

def set_openai_api_configurations():
    """
    Set OpenAI API configurations using environment variables.

    Returns:
        bool: True if configurations are applied successfully, False otherwise.
    """
    required_vars = ['OPENAI_API_KEY', 'OPENAI_DEPLOYMENT_NAME', 'OPENAI_API_BASE', 'OPENAI_API_TYPE', 'OPENAI_API_VERSION']
    if not validate_environment_variables(required_vars):
        logging.error("OpenAI API configurations are incomplete. Please check your environment variables.")
        return False

    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.api_base = os.environ['OPENAI_API_BASE']
    openai.api_type = os.environ['OPENAI_API_TYPE']
    openai.api_version = os.environ['OPENAI_API_VERSION']
    return True

def send_prompt(prompt):
    """
    Send a text prompt to the OpenAI API for completion and retrieves the response.

    Parameters:
        prompt (str): The text prompt to send.

    Returns:
        str: The text content of the API response, or None if an error occurs.
    """
    messages = [{"role": "user", "content": prompt}]
    try:
        response = openai.ChatCompletion.create(
            engine=os.environ['OPENAI_DEPLOYMENT_NAME'],
            messages=messages,
            max_tokens=200,
        )
        return str(response.choices[0].message.content.strip())
    except Exception as e:
        logging.error(f"Failed to send prompt to API: {e}")
        return None