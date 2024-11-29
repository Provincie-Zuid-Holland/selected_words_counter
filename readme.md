# Selected Words Counter

**Selected Words Counter** is a Python tool that scans various file formats within a specified directory for occurrences of specific words from a predefined list, outputting the results in an organized Excel file.

## How It Works

1. **File Conversion**: The tool automatically converts supported file formats to `.txt` for streamlined text searching.
2. **Word Count Analysis**: It then searches each converted file for the words in your word list, creating an Excel report where each column represents a word and each row represents a file, displaying the count of occurrences.

## Getting Started

### Prerequisites
- Python 3.x
- Necessary packages (see `requirements.txt`)

### Installation
Clone this repository and install the dependencies for the latest version:

```bash
git clone https://github.com/Provincie-Zuid-Holland/selected_words_counter.git
cd selected-words-counter
pip install -r requirements.txt
pip install -e .
 ```
Or install with pip:
```bash

pip install selected-words-counter

```

If you are on Windows ensure that you have either MS-Office or LibreOffice installed in the default locations for now.
So "C:\Program Files\Microsoft Office" or "C:/Program Files/LibreOffice/"

### Configuration
Customize the `config.py` file to specify:
- Your target directory
- Supported file formats
- List of words to search for

### Usage
Run the tool using:

```bash
python main.py
```

The output Excel file will be saved to the specified location, providing a summary of word counts per file.

## Unit Tests

To run unit tests on synthetic data, navigate to the `./tests` folder and run `pytest`:

```bash
cd tests
pytest
```


## Author
Michael de Winter
