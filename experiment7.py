!pip install -q openai pandas

from google.colab import userdata
from openai import OpenAI

MAX_CALLS = 40
call_count = 0

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=userdata.get("GROQ_API_KEY"),
)
MODEL = "llama-3.3-70b-versatile"


def ask_llm(prompt, system=None, temperature=0.3):
    """Send a prompt to Groq. Raises if daily call cap exceeded."""
    global call_count
    call_count += 1
    if call_count > MAX_CALLS:
        raise RuntimeError(f"Lab limit reached ({MAX_CALLS} calls). Stop and save your work.")
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

print("Setup complete. Model:", MODEL)

v=["Summarize about romeo and juliet in one paragraph", "Summarize about romeo and juliet in exactly 2 sentences. Response should be in simple english. ", "Consider your self as a romantic writer give info about Romeo and juliet in 2 sentences. Response should be in simple english. Describe the forbidden love of romeo and juliet."]
for i in v:
    print("Prompt: "+i)
    print("Response: ")
    print(ask_llm(i)+"\n")
