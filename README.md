![image](imgs/Words2World.png)

# Introduction

Words2World is a Google Docs translation tool for amateur novel writers. 

It allows users to translate their documents into multiple languages while preserving the original formatting.

# requirements
- Python 3.10 or higher
- Google Cloud Translation API credentials
- Google Docs API credentials

# Installation

Install the required dependencies using pip:
```
pip install -r requirements.txt -r requirements-dev.txt
```

# Usage

Check the version of the tool:
```
python -m wordtraductor.cli.main --version
```

Launch the translation process:
```
python -m wordtraductor.cli.main translate ...
```

# Testing
```
pytest tests/ -v
```

