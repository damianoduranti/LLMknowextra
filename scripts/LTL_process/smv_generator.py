import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_smv_files_from_json(json_file_path, output_directory):
    """
    Reads traces from a JSON file and generates SMV files for each trace, saving them to a specified directory.

    Logging is used to provide output messages about the script's progress and any potential issues encountered.

    Parameters:
    - json_file_path (str): Path to the JSON file containing the traces.
    - output_directory (str): Directory where SMV files will be saved.
    """
    def read_json_data(file_path):
        """Attempt to read and return JSON content from a specified file."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {file_path}: {e}")
            raise

    try:
        traces = read_json_data(json_file_path)
    except Exception as e:
        logging.error(f"Failed to process JSON file: {e}")
        return

    for trace_type in ['P', 'N']:
        for index, trace in enumerate(traces[trace_type], start=1):
            variables = set()
            for step in trace:
                variables.update(step)

            smv_content = "MODULE main"
            for var in sorted(variables):
                smv_content += f"\nVAR {var} : boolean;"

            trace_length = len(trace)
            smv_content += f"""
VAR End : boolean;
VAR pc : 1..{trace_length + 1};

ASSIGN
 init(pc) := 1;
 next(pc) := case
   pc <= {trace_length} : pc + 1;
   TRUE    : {trace_length + 1};
 esac;
 init(End) := FALSE;
 next(End) := case
   pc >= {trace_length} : TRUE;
   TRUE    : End;
 esac;\n
"""
            for i, step in enumerate(trace, start=1):
                conditions = ' & '.join([f"{var}" if var in step else f"!{var}" for var in sorted(variables)])
                smv_content += f"INVAR\n pc = {i} -> ({conditions})\n"

            file_name = f"{os.path.splitext(os.path.basename(json_file_path))[0]}{'_sat' if trace_type == 'P' else '_unsat'}{index}.smv"
            output_path = os.path.join(output_directory, os.path.splitext(os.path.basename(json_file_path))[0])

            os.makedirs(output_path, exist_ok=True)
            full_file_path = os.path.join(output_path, file_name)

            try:
                with open(full_file_path, 'w') as smv_file:
                    smv_file.write(smv_content)
                logging.info(f"Generated SMV file: {full_file_path}")
            except IOError as e:
                logging.error(f"Failed to write SMV file {full_file_path}: {e}")

def generate_smv_spec(parsed_response):
    """
    Generate SMV specification from parsed response and save it to a specified output file.

    Parameters:
    - parsed_response (str): Parsed response from the LLM.
    - output (str): Path to the output file where the SMV specification will be saved.
    """
    spec_content = ""
    spec_content += f"""set on_failure_script_quits;
unset forward_search;
unset ltl_tableau_forward_search;
time;
echo;
go;
time;
echo;
check_ltlspec -p "{parsed_response}";
echo;
time;
quit;
"""
    # get highest number after filename in the directory
    spec_directory = os.path.join("data", "spec")
    if not os.path.exists(spec_directory):
        os.makedirs(spec_directory)
    if os.listdir(spec_directory):
        latest = max([int(f.split(".")[0].split("spec")[1]) for f in os.listdir(spec_directory) if f.startswith("spec")])
    else:
        latest = 0
    filename = f"spec{latest + 1}"
    output_path = os.path.join("data", "spec", filename)
    try:
        with open(output_path, 'w') as spec_file:
            spec_file.write(spec_content)
        logging.info(f"Generated SMV specification: {output_path}")
        return output_path
    except IOError as e:
        logging.error(f"Failed to write SMV specification to {output_path}: {e}")
        return None

def main():
    generate_smv_spec("G((p) -> (X(F(q & !End) & !End)) | End)")

if __name__ == "__main__":
    main()