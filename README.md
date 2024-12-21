# About
Classify and sort your [Immich](https://immich.app) pictures into albums based on their content with LLMs.

## Features
- [x] User defined tags
- [x] Ollama backend
- [x] mTLS client certificates


# Installation
1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Start ollama and load a model of your choice which supports images
4. Copy `config_example.py` to `config.py` and fill the required values
5. Run `python main.py`

When done, there will be new albums prefixed with 'AI_' (by default) and all of your photos being assigned to one
of those albums
