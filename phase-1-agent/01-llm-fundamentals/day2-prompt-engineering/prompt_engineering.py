"""
Gün 2 — Prompt Engineering
===========================
Öğreneceklerin:
1. System prompt nedir (modele kim olduğunu söyleme)
2. Zero-shot vs Few-shot (örnekli vs örneksiz soru sorma)
3. Chain-of-thought (modelden adım adım düşünmesini isteme)
4. Role prompting (modele rol verme)
"""

from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.6-flash"


def guvenli_cagri(contents, config=None, system=None):
    for deneme in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config={**(config or {}), **({"system_instruction": system} if system else {})},
            )
            return response.text.strip()
        except Exception as e:
            if "429" in str(e):
                print("  [Kota doldu, 60 saniye bekleniyor...]")
                time.sleep(60)
            else:
                return f"  [Hata: {e}]"
    return "  [3 denemede de başarısız]"


# ============================================================
# DENEY 1: System Prompt
# ============================================================
# System prompt = modele "sen kimsin, nasıl davran" dediğin talimat.
# Kullanıcı mesajından ayrıdır. Modelin tüm davranışını şekillendirir.

print("=" * 60)
print("DENEY 1: System Prompt Etkisi")
print("=" * 60)

soru = "Python'da list comprehension nedir?"

# System prompt OLMADAN
print("\n--- System prompt YOK ---")
cevap = guvenli_cagri(soru)
print(f"  {cevap[:200]}...")
time.sleep(10)

# System prompt İLE — Başlangıç seviyesi öğretmen
print("\n--- System: Sen bir başlangıç seviyesi Python öğretmenisin ---")
cevap = guvenli_cagri(
    soru,
    system="Sen bir başlangıç seviyesi Python öğretmenisin. Her şeyi çok basit ve Türkçe açıkla. Teknik terim kullandığında parantez içinde tanımını ver."
)
print(f"  {cevap[:300]}...")
time.sleep(10)

# System prompt İLE — Kıdemli mühendis
print("\n--- System: Sen kıdemli bir yazılım mühendisisin ---")
cevap = guvenli_cagri(
    soru,
    system="Sen 15 yıllık deneyime sahip kıdemli bir yazılım mühendisisin. Kısa, teknik ve öz cevaplar ver. Gereksiz açıklama yapma."
)
print(f"  {cevap[:300]}...")
time.sleep(10)


# ============================================================
# DENEY 2: Zero-Shot vs Few-Shot
# ============================================================
# Zero-shot = Modele hiç örnek vermeden soru sorma
# Few-shot = Modele birkaç örnek gösterip aynı formatta cevap isteme

print("\n" + "=" * 60)
print("DENEY 2: Zero-Shot vs Few-Shot")
print("=" * 60)

# Zero-shot: Sadece görevi söyle
print("\n--- Zero-Shot ---")
cevap = guvenli_cagri(
    "Bu cümlenin duygusunu belirle: 'Bu film gerçekten çok sıkıcıydı'"
)
print(f"  {cevap[:200]}")
time.sleep(10)

# Few-shot: Örnekler ver, sonra sor
print("\n--- Few-Shot (3 örnek) ---")
cevap = guvenli_cagri(
    """Aşağıdaki örneklere bakarak cümlenin duygusunu belirle.

Örnek 1: "Harika bir gün geçirdim!" → Pozitif
Örnek 2: "Çok kötü hissediyorum" → Negatif  
Örnek 3: "Bugün hava güneşli" → Nötr

Şimdi sen belirle: "Bu film gerçekten çok sıkıcıydı" → """
)
print(f"  {cevap[:200]}")
time.sleep(10)


# ============================================================
# DENEY 3: Chain-of-Thought (Adım Adım Düşünme)
# ============================================================
# Normal soru sorduğunda model direkt cevap verir.
# "Adım adım düşün" dediğinde model akıl yürütme sürecini gösterir.
# Bu karmaşık problemlerde doğruluk oranını artırır.

print("\n" + "=" * 60)
print("DENEY 3: Chain-of-Thought")
print("=" * 60)

problem = "Bir markette 3 elma ve 2 armut aldım. Elmalar tanesi 5 TL, armutlar tanesi 8 TL. Kasada 50 TL verdim. Kaç TL para üstü alırım?"

# Normal soru
print("\n--- Normal ---")
cevap = guvenli_cagri(problem)
print(f"  {cevap[:300]}")
time.sleep(10)

# Chain-of-thought
print("\n--- Chain-of-Thought ---")
cevap = guvenli_cagri(
    problem + "\n\nAdım adım düşün. Her adımda ne hesapladığını göster."
)
print(f"  {cevap[:500]}")
time.sleep(10)


# ============================================================
# DENEY 4: Role Prompting (Rol Verme)
# ============================================================
# Aynı soruyu farklı rollerdeki modele sorduğunda farklı cevaplar alırsın.

print("\n" + "=" * 60)
print("DENEY 4: Rol Verme")
print("=" * 60)

soru_genel = "Yapay zeka insanların işini elinden alacak mı?"

roller = [
    ("Teknoloji CEO'su", "Sen bir teknoloji şirketinin CEO'susun. İyimser ve vizyon sahibisin."),
    ("Fabrika işçisi", "Sen 20 yıldır fabrikada çalışan bir işçisin. Endişeli ve pratik düşünüyorsun."),
]

for rol_adi, rol_prompt in roller:
    print(f"\n--- Rol: {rol_adi} ---")
    cevap = guvenli_cagri(soru_genel, system=rol_prompt)
    print(f"  {cevap[:300]}...")
    time.sleep(10)


# ============================================================
# ÖZET
# ============================================================
print("\n" + "=" * 60)
print("GÜN 2 ÖĞRENİLENLER")
print("=" * 60)
print("""
1. SYSTEM PROMPT: Modelin davranışını belirleyen talimat.
   Aynı soru, farklı system prompt ile tamamen farklı cevap üretir.

2. ZERO-SHOT vs FEW-SHOT:
   Zero-shot = örnek vermeden sor (basit görevler için yeterli)
   Few-shot = örneklerle sor (format ve kalite kontrolü için güçlü)

3. CHAIN-OF-THOUGHT: "Adım adım düşün" demek karmaşık
   problemlerde doğruluk oranını ciddi şekilde artırır.

4. ROLE PROMPTING: Modele rol vermek cevabın perspektifini
   ve tonunu tamamen değiştirir.
""")