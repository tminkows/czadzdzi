# PDF Question Tool

This project provides a simple script to query the OpenAI API about the
contents of a PDF file.

## Setup

1. Install dependencies (requires internet access):
   ```bash
   pip install -r requirements.txt
   ```
2. Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.

## Usage

Run the script with the path to the PDF file and your question:

```bash
python ask_open_ai.py -f "file.pdf" "Summarize the first two pages"
```

The script logs its progress and prints the assistant's answer.
