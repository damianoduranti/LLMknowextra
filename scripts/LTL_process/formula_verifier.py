import subprocess
import resource
import logging
import os
import glob
from LTL_process.smv_generator import generate_smv_spec

from LTL_process.config import NUXMV, MAX_VIRTUAL_MEMORY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def limit_virtual_memory():
    try:
        current_soft_limit, current_hard_limit = resource.getrlimit(resource.RLIMIT_AS)

        if MAX_VIRTUAL_MEMORY > current_soft_limit:
            if MAX_VIRTUAL_MEMORY <= current_hard_limit:
                resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, current_hard_limit))
                logging.info(f"Virtual memory limit set to {MAX_VIRTUAL_MEMORY}")
            else:
                logging.error("Cannot set virtual memory limit above the hard limit")
        else:
            pass
    except ValueError as e:
        logging.error(f"Failed to set virtual memory limit: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while setting virtual memory limit: {e}")

def formula_verifier(fname, script, timeout=None, use_sat=False):
    # subprocess.Popen('ulimit -v 1024; ls', shell=True)
    command = list([NUXMV])
    command.append("-int")
    command.append("-source")
    command.append(script)
    command.append(fname)
    nfn = ""
    if use_sat:
        nfn = fname + "_sat_out"
    else:
        nfn = fname + "_bdd_out"
    try:
        result = subprocess.run(command,
                                shell=False,
                                stdout=subprocess.PIPE,
                                timeout=timeout,
                                preexec_fn=limit_virtual_memory)
        if (result.returncode != 0):
            logging.error("Failure running {}.".format(fname))
            return 1
        else:
            with open(nfn, "w") as o:
                o.write(result.stdout.decode('utf-8'))
                if result.stderr is not None:
                    o.write(result.stderr.decode('utf-8'))
                logging.info("Succeded in analyzing {}.".format(fname))
    except OSError as error:
        logging.error("Some problems running {}: {}".format(fname, str(error)))
        return 1
    except subprocess.TimeoutExpired as err:
        with open(nfn, "w") as o:
            o.write("Timeout: {}\n".format(timeout))
        logging.warning("Timeout for {}: {}".format(fname, str(err)))
        return 1
    return nfn
    pass

def evaluator(directory, script_path):
    """
    Verifies LTL formulas in a batch.
    
    Parameters:
    - directory (str): Directory containing smv traces.

    Returns:
    - list: List of evaluation results.
    """
    results_sat = []
    results_unsat = []
    for file_path in sorted(glob.glob(os.path.join(directory, '*.smv'))):
        result_path = formula_verifier(file_path, script_path)
        if "_sat" in str(file_path):
            with open(result_path, "r") as f:
                result = f.read()
                if "true" in result:
                    results_sat.append(True)
                elif "false" in result:
                    results_sat.append(False)
        elif "_unsat" in str(file_path):
            with open(result_path, "r") as f:
                result = f.read()
                if "true" in result:
                    results_unsat.append(True)
                elif "false" in result:
                    results_unsat.append(False)
    error = None
    if not all(results_sat):
        error = "Candidate evaluation failed [some positive traces do not satisfy the formula]."
    if any(results_unsat):
        error = "Candidate evaluation failed [some negative traces satisfy the formula]."
    return all(results_sat) and not any(results_unsat), error

def main():
    path = "data/LTL_process/traces_smv/LTL_constrained/1.1/1.1_sat1.smv"
    script_path = generate_smv_spec("G((p) -> (X(F(q & !End) & !End)) | End)")
    print(evaluator("data/LTL_process/traces_smv/LTL_constrained/1.1", script_path))

if __name__ == "__main__":
    main()