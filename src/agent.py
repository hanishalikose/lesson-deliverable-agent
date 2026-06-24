import os, sys
from datetime import date
from src.audit import load_file, audit_lesson, ROOT
from src.summarize import summarize_lesson

def run(path: str):
    print(f"Loading: {path}")
    text = load_file(path)

    print("Running audit...")
    audit = audit_lesson(text)

    print("Running summary...")
    summary = summarize_lesson(text)

    today = date.today().strftime("%m%d")
    base = os.path.splitext(os.path.basename(path))[0].split()[0]

    out_dir = os.path.join(ROOT, "outputs")
    os.makedirs(out_dir, exist_ok=True)

    summary_path = os.path.join(out_dir, f"{today}_{base}_Han.md")
    audit_path = os.path.join(out_dir, f"{today}_{base}_audit.md")

    with open(summary_path, "w") as f:
        f.write(summary)
    with open(audit_path, "w") as f:
        f.write("# Accuracy Audit\n\n" + audit)

    print(f"\nWrote summary: {summary_path}")
    print(f"Wrote audit:   {audit_path}")
    return summary_path, audit_path

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "inputs/lesson.md"
    run(path)