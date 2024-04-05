# LLMknowsynth

## Project Structure

This project is organized as follows:

```
.
├── config/
│   └── api_keys.json
│
├── nuXmv/
│   └── bin/
│       └── nuXmv
│
├── data/
│   ├── traces_json/
│   │   ├── LTL_constrained/
│   │   │   └── *.json
│   │   └── LTL_unconstrained/
│   │       └── *.json
│   │
│   └── traces_smv/
│       ├── LTL_constrained/
│       │   └── *.smv
│       └── LTL_unconstrained/
│           └── *.smv
│
├── scripts/
│   ├── formula_translator.py
│   ├── formula_verifier.py
│   ├── llm_utils.py
│   ├── prompt_generator.py
│   └── smv_generator.py
│
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

Duplicate the config/api_keys.json.example file and rename the duplicate to config/api_keys.json.
Open config/api_keys.json and fill in your actual API keys in place of the placeholder values provided.

Additionally, to set up the nuXmv tool:

Download the nuXmv executable from the official source.
Create a new directory named nuXmv within your project's root directory.
Inside the nuXmv directory, create a subdirectory named bin.
Place the downloaded nuXmv executable inside the nuXmv/bin directory.
