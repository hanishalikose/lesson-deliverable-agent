import sys
import os
from datetime import date
from src.audit import client, load_file

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def summarize_lesson(lesson_text: str) -> str:
    with open(os.path.join(ROOT, "prompts", "summary_prompt.md")) as f:
        system_prompt = f.read()
    today = date.today().strftime("%d.%m.%Y")
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Today's date is {today}.\n\nLesson:\n{lesson_text}"},
        ],
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "inputs/lesson.md"
    print(summarize_lesson(load_file(path)))