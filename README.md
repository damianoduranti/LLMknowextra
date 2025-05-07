# LLM-Driven Knowledge Extraction: Results in Temporal and Description Logics

Duranti, D., Giorgini, P., Mazzullo, A., Robol, M., Roveri, M. (2025). LLM-Driven Knowledge Extraction in Temporal and Description Logics. In: Alam, M., Rospocher, M., van Erp, M., Hollink, L., Gesese, G.A. (eds) Knowledge Engineering and Knowledge Management. EKAW 2024. Lecture Notes in Computer Science(), vol 15370. Springer, Cham. https://doi.org/10.1007/978-3-031-77792-9_12

## Table of Contents

- [Abstract](#abstract)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)

## Abstract

Trustworthy knowledge extraction represents a bottleneck in the development of autonomous AI agents capable of integrating learning and reasoning capabilities. As a foundational framework of neuro-symbolic knowledge acquisition systems from semi-structured data, we introduce an approach
that combines Large Language Model (LLM) functionalities with symbolic verification modules. In a process mining context, we propose to leverage LLMs to generate linear temporal logic specifications starting from sets of finite traces that represent event logs. In a knowledge representation setting, we focus instead on LLM-based extraction of description logic concepts to obtain human-readable conceptualizations that separate positive and negative labeled data instances. We integrate chat interfaces based on state-of-the-art LLMs with formal verification modules: In the process mining case, we employ model checking tools for linear temporal logic on finite traces; and, for description logic concept learning, we perform entailment checks using dedicated reasoning engines. First, we perform a proof-of-concept evaluation of these architectures, comparing the performance of the LLMs on each task. We then provide an implementation of a GPT-based toolchain to automate the candidate generation and verification steps.

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
│   ├── dl_concept.py
│   ├── dl_trace_gen.py
│   ├── llm_utils.py
│   ├── ltl_process.py
│   ├── ltl_trace_gen.py
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
git clone https://github.com/damianoduranti/LLMknowextra.git
cd LLMknowextra
pip install -r requirements.txt
```

## Configuration

1. **API keys:** Duplicate ```config/api_keys.json.example``` to ```config/api_keys.json``` and fill in your actual API keys.
2. **nuXmv setup:** Download the [nuXmv](https://nuxmv.fbk.eu/) and place the nuXmv executable inside the ```nuXmv/bin``` directory.

### Special Instructions for Apple Silicon Devices

nuXmv may require the x86 version of the GMP library on Apple Silicon devices. Follow these steps to install the x86 version of Homebrew and GMP:

1. Install Homebrew for x86:
Open Terminal and run the following command to install the x86 version of Homebrew in /usr/local (native ARM installation is in /opt/brew):
```
bash arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```
2. Install GMP for x86:
After the x86 Homebrew installation is complete, install GMP by executing:
```
bash arch -x86_64 /bin/bash -c "/usr/local/bin/brew install gmp"
```

> The x86 installations are necessary to ensure compatibility with software that has not yet been updated to fully support ARM architecture.

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
