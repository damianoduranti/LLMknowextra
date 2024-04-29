# LLM-Driven Knowledge Extraction: Results in Temporal and Description Logics

> Damiano Duranti, Paolo Giorgini, Andrea Mazzullo, Marco Robol and Marco Roveri

## Table of Contents

- [Abstract](#abstract)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)

## Abstract

In the quest to surmount the challenges of knowledge extraction which is crucial for the development of autonomous AI agents with integrated learning and reasoning capabilities, we introduce a neuro-symbolic framework for knowledge acquisition systems. This foundational framework combines the functionalities of Large Language Models (LLMs) with symbolic verification modules to process semi-structured data efficiently. Our approach involves leveraging LLMs to generate linear temporal logic specifications from finite trace sets representing event logs in a process mining context. Simultaneously, in a knowledge representation setting, we utilize LLMs to extract description logic concepts, achieving human-readable conceptualizations that distinctively categorize positive and negative data instances. The integration of chat interfaces based on state-of-the-art LLMs with formal verification modules is pivotal in our system. For process mining, we employ model checking tools for linear temporal logic on finite traces, and for description logic concept learning, we perform entailment checks using dedicated reasoning engines. Following a proof-of-concept evaluation, the performance of LLMs on each task was analyzed, leading to the development of a GPT-based toolchain that automates the generation and verification steps in these knowledge extraction processes.

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
│   │   ├── strong_sep/
│   │   │   └── */
│   │   │       ├── *_ontology.owl
│   │   │       └── *_instances.json
│   │   └── weak_sep/
│   │       └── */
│   │           ├── *_ontology.owl
│   │           └── *_instances.json
│   └── LTL_process/
│       ├── unconstrained/
│       │   └── *.json
│       └── constrained/
│           └── *.json
│
├── output/
│   ├── DL_concept/
│   │   ├── strong_sep/
│   │   │   └── */
│   │   │       ├── *_ontology.owl
│   │   │       └── *_instances.json
│   │   └── weak_sep/
│   │       └── */
│   │           ├── *_ontology.owl
│   │           └── *_instances.json
│   └── LTL_process/
│       ├── unconstrained/
│       │   └── */
│       │       ├── results/
│       │       │   └── attempt.txt
│       │       ├── spec/
│       │       │   └── spec
│       │       └── traces_smv/
│       │           └── *.smv
│       └── constrained/
│           └── */
│               ├── results/
│               │   └── attempt.txt
│               ├── spec/
│               │   └── spec
│               └── traces_smv/
│                   └── *.smv
│
├── scripts/
│   ├── DL_concept/
│   │   └── concept_verifier.py
│   ├── LTL_process/
│   │   ├── translator/
│   │   │   ├── parsers/
│   │   │   │   ├── base.py
│   │   │   │   ├── ltl.lark
│   │   │   │   ├── ltl.py
│   │   │   │   └── pl.lark
│   │   │   ├── syntax/
│   │   │   │   └── ltl.py
│   │   │   ├── formula_translator.py
│   │   │   └── utils.py
│   │   ├── config.py
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

### Folders

- **`data/`**:
  - **`DL_concept/`**: Contains datasets for Description Logic (DL) concept learning. It is divided into:
    - **`strong_sep/`** and **`weak_sep/`**: These subdirectories store ontology files (`*_ontology.owl`) and instance data (`*_instances.json`) categorized by their conceptual separation strength.
  - **`LTL_process/`**: Stores data for Linear Temporal Logic (LTL) processes, categorized into:
    - **`unconstrained/`** and **`constrained/`**: Include JSON files representing sets of finite traces used for generating LTL specifications.

- **`output/`**: This directory mirrors the `data/` structure and stores outputs from the DL concept learning and LTL process analysis, including results, specifications, and SMV files for model checking.

- **`scripts/`**:
  - **`DL_concept/`**: Scripts for verifying and processing description logic concepts.
  - **`LTL_process/`**: Utilities and scripts for translating, verifying, and generating specifications for LTL processes.
    - **`translator/`**:
      - **`parsers/`**: Contains parsers for different logic formats.
      - **`syntax/`**: Scripts related to the syntactic elements of logic expressions.

## Installation

Instructions on how to get your project up and running on a local machine for development and testing purposes.

```bash
git clone https://github.com/damianoduranti/LLMknowsynth.git
cd LLMknowsynth
pip install -r requirements.txt
```

## Configuration

1. **API keys:** Duplicate ```config/api_keys.json.example``` to ```config/api_keys.json``` and fill in your actual API keys.
2. **nuXmv setup:** Download the [nuXmv](https://nuxmv.fbk.eu/) and place the nuXmv executable inside the ```nuXmv/bin``` directory.

## Usage

Run the following scripts within the ```scripts/``` directory to process data on all the input files found in ```data``` folder:

```bash
python scripts/dl_concept.py
```

```bash
python scripts/ltl_process.py
```

### Prerequisites

- Python 3.7+
- nuXmv executable for LTL verification
- Java installed for DL verification
- Required Python packages listed in requirements.txt

## Acknowledgements

- [nuXmv](https://nuxmv.fbk.eu/)
- [Owlready2](https://github.com/pwin/owlready2)
- [pylogics](https://github.com/whitemech/pylogics)
