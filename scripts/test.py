from prompt_generator import *
from llm_utils import *

logging.basicConfig(level=logging.INFO)

def main():

    # DL concept prompt generation
    prompt = generate_dl_prompts_from_json('data/DL_concept/1/1_instances.json', 'data/DL_concept/1/1_ontology.owl', separation_type='strong')

    #print(prompt)

    # load_api_keys()
    # set_openai_api_configurations()
    
    # logging.info("Sending prompt to OpenAI API...")
    # print(send_prompt(prompt))
    response = """
    with onto:
        class C(Thing):
                equivalent_to = [Student & (studiesAt.some(EuUni))]"""
    
    

if __name__ == '__main__':
    main()