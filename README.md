# PDF Question Tool

This project provides a simple script to query the OpenAI API about the
contents of a PDF file.

## Setup

1. Install dependencies (requires internet access):
   ```bash
   pip install -r requirements.txt
   ```
2. Create a file named `api_key` in this directory containing your OpenAI API key.

## Usage

Run the script with the path to the PDF file and your question. The script will
automatically read the API key from the `api_key` file:

```bash
python ask_open_ai.py -f "file.pdf" "Summarize the first two pages"
```

The script logs its progress and prints the assistant's answer.
