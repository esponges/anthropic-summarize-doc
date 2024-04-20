import os

from PyPDF2 import PdfReader

import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

def summarize_pdf(path: str) -> str:
    doc_path = os.getenv("DOC_PATH")
    reader = PdfReader(doc_path)
    text = "\n".join([page.extract_text() for page in reader.pages])

    no_tokens = anthropic_client.count_tokens(text)
    print(f"Number of tokens in text: {no_tokens}")

    # if no_tokens > 100000:
    #     raise ValueError(f"Text is too long {no_tokens}.")

    prompt = f"{anthropic.HUMAN_PROMPT}: Summarize the following text in ~900 words (3 pages), should be readable:\n\n{text}\n\n{anthropic.AI_PROMPT}:\n\nSummary"
    res = anthropic_client.completions.create(prompt=prompt, model="claude-3-opus-20240229", max_tokens_to_sample=2500)
    # res = anthropic_client.


    return res["completion"]

summarize_pdf("/Users/fertostado/downloads/Documento Mtro.Chanona.pdf")
