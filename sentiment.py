import google.generativeai as genai
from config import api_key

# Konfigurasi API key
genai.configure(api_key=api_key)

def analyze_sentiment(message):
    sentiment_prompt = f"""
    Tell me whether the following sentence's sentiment is positive, negative, or neutral.
    Sentence: "{message}"
    Sentiment:"""

    sentiment_response = genai.generate_text(
        model='models/text-bison-001',
        temperature=0.5,
        candidate_count=1,
        top_k=40,
        top_p=0.95,
        max_output_tokens=1024,
        prompt=sentiment_prompt
    )

    return sentiment_response.result.strip().lower()
