import argparse
import logging
import os

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
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"{question}\n\nDocument text:\n{text}",
        },
    ]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    logging.info("Received response from OpenAI")
    return response["choices"][0]["message"]["content"]


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
