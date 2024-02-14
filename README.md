# LLMknowsynth

## Project Structure

This project is organized as follows:

```
.
├── config/
│   └── api_keys.json.example
│
├── data/
│   ├── LTL_constrained/
│   │   └── *.json
│   │ 
│   └── LTL_unconstrained/
│       └── *.json
│
├── scripts/
│   └── prompt_generator.py
│
├── tests/
│   └── prompt_generator_tests.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Installation

Instructions on how to get your project up and running on a local machine for development and testing purposes.

```bash
git clone https://github.com/yourusername/yourprojectname.git
cd LLMknowsynth
pip install -r requirements.txt
```

## Configuration

Before running the scripts, you need to set up the necessary API keys:

Copy config/api_keys.json.example to config/api_keys.json.
Replace the placeholder values in config/api_keys.json with your actual API keys.
