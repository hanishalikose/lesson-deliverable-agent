import os, sys
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ["GROQ_API_KEY"])

def audit_lesson(lesson_text: str) -> str:
    with open("prompts/audit_prompt.md") as f:
        system_prompt = f.read()
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": lesson_text},
        ],
    )
    return resp.choices[0].message.content

def load_file(path: str, max_chars: int = 20000) -> str:
    if path.lower().endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(path)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        with open(path) as f:
            text = f.read()
    if len(text) > max_chars:
        print(f"[truncated from {len(text)} to {max_chars} chars to fit free-tier limit]")
        text = text[:max_chars]
    return text

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "inputs/lesson.md"
    print(audit_lesson(load_file(path)))