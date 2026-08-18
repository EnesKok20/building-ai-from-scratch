"""
Gün 1 — Tokenization ve LLM Temelleri
"""
from google import genai
import time
import os
from dotenv import load_dotenv
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.6-flash"


def guvenli_cagri(contents, config=None):
    """API çağrısı yap, kota hatası gelirse bekle ve tekrar dene."""
    for deneme in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL, contents=contents, config=config,
            )
            return response.text.strip()
        except Exception as e:
            if "429" in str(e):
                print("  [Kota doldu, 60 saniye bekleniyor...]")
                time.sleep(60)
            else:
                return f"  [Hata: {e}]"
    return "  [3 denemede de başarısız]"


# DENEY 1: Token Sayma
print("=" * 60)
print("DENEY 1: Token Sayma")
print("=" * 60)

test_cumleler = [
    "Merhaba",
    "Merhaba dünya",
    "Yapay zeka dünyayı değiştirecek",
    "AI engineering is the fastest growing field in 2026",
    "Karadeniz Teknik Üniversitesi Yazılım Mühendisliği",
]

for cumle in test_cumleler:
    result = client.models.count_tokens(model=MODEL, contents=cumle)
    print(f"  '{cumle}' → {result.total_tokens} token")

# DENEY 2: Temperature
print("\n" + "=" * 60)
print("DENEY 2: Temperature Etkisi")
print("=" * 60)

for temp in [0.0, 1.0]:
    print(f"\n--- Temperature: {temp} ---")
    cevap = guvenli_cagri(
        "Yapay zeka nedir? Tek cümleyle açıkla.",
        config={"temperature": temp},
    )
    print(f"  {cevap}")
    time.sleep(10)

# DENEY 3: max_output_tokens
print("\n" + "=" * 60)
print("DENEY 3: max_output_tokens Etkisi")
print("=" * 60)

for max_tokens in [20, 200]:
    cevap = guvenli_cagri(
        "Python programlama dilinin avantajlarını açıkla.",
        config={"max_output_tokens": max_tokens},
    )
    print(f"\n--- max_output_tokens: {max_tokens} ---")
    print(f"  {cevap}")
    time.sleep(10)

# ÖZET
print("\n" + "=" * 60)
print("GÜN 1 ÖĞRENİLENLER")
print("=" * 60)
print("""
1. TOKEN: Modelin metni gördüğü en küçük birim.
2. TEMPERATURE: 0.0 = deterministik, 1.0 = yaratıcı
3. MAX_OUTPUT_TOKENS: Cevap uzunluk limiti
""")