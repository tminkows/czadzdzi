import argparse
import logging
import os


def load_api_key(path: str) -> str:
    """Load an API key from a file."""
    try:
        with open(path, "r", encoding="utf-8") as fp:
            key = fp.read().strip()
    except FileNotFoundError as exc:
        raise RuntimeError(f"API key file '{path}' not found") from exc
    if not key:
        raise RuntimeError(f"API key file '{path}' is empty")
    return key

import openai
from pdfminer.high_level import extract_text


def extract_pdf_text(pdf_path: str) -> str:
    """Extract all text from a PDF file."""
    with open(pdf_path, "rb") as fp:
        return extract_text(fp)


def ask_openai_about_pdf(pdf_path: str, question: str) -> str:
    """Send the text of a PDF and a question to OpenAI and return the response."""
    logging.info("Extracting text from %s", pdf_path)
    text = extract_pdf_text(pdf_path)

    logging.info("Sending request to OpenAI API")
    api_key_path = os.path.join(os.path.dirname(__file__), "api_key")
    client = openai.OpenAI(api_key=load_api_key(api_key_path))

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"{question}\n\nDocument text:\n{text}",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
    logging.info("Received response from OpenAI")
    return response.choices[0].message.content


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask OpenAI a question about a PDF")
    parser.add_argument("-f", "--file", required=True, help="Path to PDF file")
    parser.add_argument("question", help="Question to ask about the PDF")
    args = parser.parse_args()

    answer = ask_openai_about_pdf(args.file, args.question)
    print(answer)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()
