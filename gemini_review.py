import google.generativeai as genai
import os
import re
from pathlib import Path

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

diff_dir = Path("diffs")
review_content = ["## Code Review"]

for diff_file in diff_dir.glob("*.diff"):
    with open(diff_file, "r") as f:
        diff = f.read()
    
    # Extract filename from diff header
    filename_match = re.search(r'^diff --git a/(.+?) b/', diff, re.MULTILINE)
    filename = filename_match.group(1) if filename_match else diff_file.stem

    response = model.generate_content(
        f"""You are a senior code reviewer. Analyze the provided code diff for: code quality, security issues, best practices, and potential bugs. Provide specific feedback with line numbers and suggestions. {diff}"""
    )
    
    review_content.append(f"### 📄 File: {filename}\n\n{response.text}\n\n---")

with open("review.md", "w") as f:
    f.write("\n".join(review_content))
