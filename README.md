# LLMknowsynth

## Project Structure

This project is organized as follows:

```text
.
├── config/
│   └── api_keys.json
│
├── nuXmv/
│   └── bin/
│       └── nuXmv
│
├── data/
│   ├── DL_concept/
│   │   └── */
│   │       ├── *_instances.json
│   │       └── *_ontology.owl
│   └── LTL_process/
│       ├── traces_json/
│       │   ├── LTL_constrained/
│       │   │   └── *.json
│       │   └── LTL_unconstrained/
│       │       └── *.json
│       └── traces_smv/
│           ├── LTL_constrained/
│           │   └── *.smv
│           └── LTL_unconstrained/
│                └── *.smv
│
├── scripts/
│   ├── DL_concept/
│   │   └── concept_verifier.py
│   ├── LTL_process/
│   │   ├── translator/
│   │   ├── config.py
│   │   ├── formula_translator.py
│   │   ├── formula_verifier.py
│   │   └── smv_generator.py
│   ├── llm_utils.py
│   └── prompt_generator.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Installation

Instructions on how to get your project up and running on a local machine for development and testing purposes.

```bash
git clone https://github.com/damianoduranti/LLMknowsynth.git
cd LLMknowsynth
pip install -r requirements.txt
```

## Configuration

Before running the scripts, you need to set up the necessary API keys:

1. Duplicate the config/api_keys.json.example file and rename the duplicate to config/api_keys.json.
2. Open config/api_keys.json and fill in your actual API keys in place of the placeholder values provided.

Additionally, to set up the nuXmv tool:

1. Download the nuXmv executable from the official source.
2. Create a new directory named nuXmv within your project's root directory.
3. Inside the nuXmv directory, create a subdirectory named bin.
4. Place the downloaded nuXmv executable inside the nuXmv/bin directory.

## Usage

1. Input data files in the appropriate format are in the data/traces_json directory.
2. Run the desired script from the scripts directory, providing the necessary arguments.

## Prerequisites

- Python 3.7+
- nuXmv executable
- Required Python packages listed in requirements.txt

## Data Formats

- JSON files in the data/traces_json directory should follow the specified schema.
- SMV files in the data/traces_smv directory should adhere to the nuXmv syntax.

## Acknowledgements

- nuXmv - Symbolic model checker used in this project.
- pylogics - Modified modules for LTL verification
- OpenAI - Language model API used for concept verification.
