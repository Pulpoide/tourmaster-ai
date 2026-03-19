import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI() #      Asegúrate de tener OPENAI_API_KEY en tu .env

DOMAINS = {
    "booking": """
        Base de datos de bares, clubes de música en vivo y centros culturales en Córdoba, Rosario y Buenos Aires. 
        Incluye nombres de lugares, géneros musicales preferidos (Rock, Jazz, Indie, DJ sets), capacidad (público), 
        información de contacto ficticia y si el lugar suele proveer sonido (backline).
    """,
    "logistics": """
        Guía de logística para músicos. Incluye tablas de consumo promedio de combustible para vehículos comunes (Partner, Kangoo, Sprinter). 
        Listado de hoteles y hostales en ciudades principales de Argentina que cuentan con cochera o estacionamiento seguro 
        para vehículos con equipamiento. Consejos para estiba de instrumentos y seguridad en ruta.
    """,
    "marketing": """
        Manual de marketing para artistas independientes. Cómo redactar una 'Gacetilla de Prensa' efectiva. 
        Plantillas de mensajes para radios y prensa local. Estrategias de promoción en Instagram y TikTok 
        específicamente para fechas de giras. Calendarios editoriales sugeridos para antes y después del show.
    """
}

def generate_docs():
    # Crear carpeta data si no existe
    if not os.path.exists("data"):
        os.makedirs("data")

    for folder, description in DOMAINS.items():
        path = f"data/{folder}_docs"
        os.makedirs(path, exist_ok=True)
        print(f"-> Generando contenido para: {folder}...")
        
        # Generamos 10 archivos por dominio para asegurar variedad y volumen (chunks)
        for i in range(10): 
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user", 
                    "content": f"Actúa como un experto en la industria musical argentina. Escribe un documento técnico sobre: {description}. Parte {i+1}/10. Usa formato Markdown con títulos y tablas si es necesario."
                }]
            )
            with open(f"{path}/doc_{i}.md", "w", encoding="utf-8") as f:
                f.write(response.choices[0].message.content)

if __name__ == "__main__":
    generate_docs()
    print("\n¡Listo! Carpetas creadas y documentos generados en /data.")