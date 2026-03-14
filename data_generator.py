import os
import time
from openai import OpenAI, APIConnectionError
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

DOMAINS = {
    "booking": "Base de datos de bares y clubes de música en Córdoba, Rosario y Buenos Aires. Incluye nombres, géneros (Rock, Jazz, Indie, DJ), capacidad y contacto.",
    "logistics": "Guía de logística para músicos: consumo de nafta (Partner/Kangoo), hoteles con cochera en Argentina y consejos de seguridad vial.",
    "marketing": "Manual de marketing: cómo redactar Gacetillas de Prensa, estrategias de Instagram/TikTok para fechas y planes de promoción local.",
}


def generate_docs():
    if not os.path.exists("data"):
        os.makedirs("data")

    for folder, description in DOMAINS.items():
        path = f"data/{folder}_docs"
        os.makedirs(path, exist_ok=True)

        for i in range(10):
            file_path = f"{path}/doc_{i}.md"

            # Si el archivo ya existe, lo saltamos para no gastar saldo
            if os.path.exists(file_path):
                continue

            print(f"-> Generando {folder} - parte {i + 1}/10...")

            success = False
            retries = 3
            while not success and retries > 0:
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "user",
                                "content": f"Actúa como experto en industria musical argentina. Escribe un documento técnico sobre: {description}. Parte {i + 1}/10. Formato Markdown.",
                            }
                        ],
                    )
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(response.choices[0].message.content)
                    success = True
                except APIConnectionError:
                    print(
                        f"   ⚠️ Error de conexión. Reintentando en 5 segundos... (Intentos restantes: {retries})"
                    )
                    time.sleep(5)
                    retries -= 1
                except Exception as e:
                    print(f"   ❌ Error inesperado: {e}")
                    break


if __name__ == "__main__":
    generate_docs()
    print("\n✅ ¡Proceso finalizado con éxito!")
