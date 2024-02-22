# LLMknowsynth

## Project Structure

This project is organized as follows:

```
.
├── config/
│   └── api_keys.json.example
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
│   ├── llm_communicator.py
│   ├── prompt_generator.py
│   └── trace_verifier.py
│
├── tests/
│   └── tests.py
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

Copy config/api_keys.json.example to config/api_keys.json.
Replace the placeholder values in config/api_keys.json with your actual API keys.
