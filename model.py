import google.generativeai as genai
from config import generation_config, system_instruction, api_key

# Konfigurasi API key
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=system_instruction
)
