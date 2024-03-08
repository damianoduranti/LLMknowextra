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
    elif formula.startswith("(weak_next "):
        subformula = formula[11:-1]
        return f"!X!({f2i(subformula)} & !End)"
    elif formula.startswith("(and "):
        formula = formula[5:-1]
        if formula[0] == "(":
            subformula1 = formula[1:formula.index(") ")]
            subformula2 = formula[formula.index(") ") + 2:]
        else:
            subformula1 = formula[:formula.index(" ")]
            subformula2 = formula[formula.index(" ") + 1:]
        return f"({f2i(subformula1)} & {f2i(subformula2)})"
    elif formula.startswith("(or "):
        formula = formula[4:-1]
        if formula[0] == "(":
            subformula1 = formula[1:formula.index(") ")]
            subformula2 = formula[formula.index(") ") + 2:]
        else:
            subformula1 = formula[:formula.index(" ")]
            subformula2 = formula[formula.index(" ") + 1:]
        return f"({f2i(subformula1)} | {f2i(subformula2)})"
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
response2 = "G(G(F(p)))"
response3 = "(X[!](p U q)) U (r U (G(s)))"
response4 = "G((p & q) -> (p | q))"
response5 = "(p -> q) U (r U s)"
parsed_response = parse_response(response)
parsed_response1 = parse_response(response1)
parsed_response2 = parse_response(response2)
parsed_response3 = parse_response(response3)
parsed_response4 = parse_response(response4)
parsed_response5 = parse_response(response5)

#logging.info(f"Formula: {parsed_response}")
print(f2i(parsed_response))
print(f2i(parsed_response1))
print(f2i(parsed_response2))
print(f2i(parsed_response3))
print(f2i(parsed_response4))
print(f2i(parsed_response5))


