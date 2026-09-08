from dotenv import load_dotenv
from google import genai
# regular expression library (part of Python standard library)
import re

load_dotenv()

client = genai.Client()


def generate_prompt():
    return f"""write the python code to calculate
a loan payment with the following inputs: interest,
term, present value. return code only wrapped in a Markdown 
code block (triple backticks). Do not add any extra text or 
explanation outside the code block."""

# other models to try if this flakes out:
# gemini-2.5-flash
# gemini-2.5-flash-lite
# gemini-3-flash

response = client.models.generate_content(
    model = "gemini-3.1-flash-lite",
    contents = generate_prompt()
)

print("--- Extracted Code ---")
print(response.text)

# use regular expression to isolate actual code
# "capture groups" are between () see regex101.com to try
match = re.search(r"```(?:\w+)?\n([\w\W]*?)```", response.text,
                  re.DOTALL)

code = match.group(1).strip()

# write to file
with open("loan_pmt.py", "w") as f:
    f.write(code)
    f.close()



