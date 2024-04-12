from llm_utils import *
from translator.utils import *
from scripts.LTL_process.smv_generator import *
from translator.parsers.ltl import parse_ltl

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def f2i(response):
    """
    Parses the response from the LLM.
    
    Parameters:
    - response (str): Response from the LLM.
    
    Returns:
    - str: Parsed response to f2i.
    """
    parsed_response = to_f2i(parse_ltl(response))
    
    return str(parsed_response)

response = "G (p -> X F q)"
response1 = "(F(p) & !(G(s))) U (q & (r -> !(X (F(t)))))"
response2 = "G(G(F(p)))"
response3 = "(X(p U q)) U (r U (G(s)))"
response4 = "G((p & q) -> (p | q))"
response5 = "(p -> q) U (r U s)"
response6 = "X(p) & N(q)"
parsed_response = f2i(response)
parsed_response1 = f2i(response1)
parsed_response2 = f2i(response2)
parsed_response3 = f2i(response3)
parsed_response4 = f2i(response4)
parsed_response5 = f2i(response5)
parsed_response6 = f2i(response6)

logging.info(f"Formula: {parsed_response}")
logging.info(f"Formula: {parsed_response1}")
logging.info(f"Formula: {parsed_response2}")
logging.info(f"Formula: {parsed_response3}")
logging.info(f"Formula: {parsed_response4}")
logging.info(f"Formula: {parsed_response5}")
logging.info(f"Formula: {parsed_response6}")

