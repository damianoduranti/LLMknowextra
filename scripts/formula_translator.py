from pylogics.parsers import parse_ltl
from llm_utils import *
from prompt_generator import *
from smv_generator import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_response(response):
    """
    Parses the response from the LLM.
    
    Parameters:
    - response (str): Response from the LLM.
    
    Returns:
    - str: Parsed response.
    """
    parsed_response = parse_ltl(response)
    logging.info(f"Parsed response: {parsed_response}")
    
    return str(parsed_response)

def f2i(formula):
    """
    Translates a formula using the end-of-time translation.
    
    Parameters:
    - formula (str): Formula to be translated.
    
    Returns:
    - str: Translated formula.
    """
    if formula[0].isalpha():
        return formula
    elif formula.startswith("(not "):
        subformula = formula[5:-1]
        return f"!{f2i(subformula)}"
    elif formula.startswith("(always "):
        subformula = formula[8:-1]
        return f"G({f2i(subformula)} | End)"
    elif formula.startswith("(eventually "):
        subformula = formula[12:-1]
        return f"F({f2i(subformula)} & !End)"
    elif formula.startswith("(next "):
        subformula = formula[6:-1]
        return f"X({f2i(subformula)} & !End)"
    elif formula.startswith("(implies "):
        formula = formula[9:-1]
        if formula[0] == "(":
            subformula1 = formula[1:formula.index(") ")]
            subformula2 = formula[formula.index(") ") + 2:]
        else:
            subformula1 = formula[:formula.index(" ")]
            subformula2 = formula[formula.index(" ") + 1:]
        return f"({f2i(subformula1)} -> {f2i(subformula2)})"
    elif formula.startswith("(until "):
        formula = formula[7:-1]
        if formula[0] == "(":
            subformula1 = formula[1:formula.index(") ")]
            subformula2 = formula[formula.index(") ") + 2:]
        else:
            subformula1 = formula[:formula.index(" ")]
            subformula2 = formula[formula.index(" ") + 1:]
        return f"({f2i(subformula1)} U ({f2i(subformula2)} & !End))"

response = "G (p -> X[!] F q)"
response1 = "p U (X[!] q)"
parsed_response = parse_response(response1)
logging.info(f"Formula: {parsed_response}")
print(f2i(parsed_response))


