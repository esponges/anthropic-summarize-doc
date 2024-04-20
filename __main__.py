import os

from PyPDF2 import PdfReader

import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
anthropic_client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

def summarize_pdf(path: str, strategy: str = "completion") -> str:
    reader = PdfReader(path)
    text = "\n".join([page.extract_text() for page in reader.pages])

    no_tokens = anthropic_client.count_tokens(text)
    print(f"Number of tokens in text: {no_tokens}")

    # if no_tokens > 100000:
    #     raise ValueError(f"Text is too long {no_tokens}.")
    res = None

    if strategy == "completion":
      prompt = f"{anthropic.HUMAN_PROMPT}: Summarize the following text in ~1600 words (3 pages), should be readable and in the language of the text:\n\n{text}\n\n{anthropic.AI_PROMPT}:\n\nSummary"
      res = anthropic_client.completions.create(prompt=prompt, model="claude-2.1", max_tokens_to_sample=2500)
    elif strategy == "messages":
      res = anthropic_client.messages.create(
         model="claude-3-opus-20240229",
         max_tokens=2500,
         messages=[
            {
              "role": "user",
              "content": f"Summarize the following text in ~1600 words (3 pages), should be readable and in spanish:\n\n{text}\n\n"
            }
         ]
      )
    else:
      raise ValueError(f"Unknown strategy {strategy}.")

    text = res.completion if strategy == "completion" else res.content[0].text

    print(text)

    return text
    
doc_path = os.getenv("DOC_PATH")

summarize_pdf(doc_path)
