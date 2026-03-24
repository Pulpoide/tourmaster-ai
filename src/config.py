import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langfuse.callback import CallbackHandler

load_dotenv()

CHROMA_PATH = "chroma_db"
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

langfuse_handler = CallbackHandler(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST"),
)

if langfuse_handler.auth_check():
    print("✅ Observabilidad: Langfuse conectado y listo para trazar.")
else:
    print("❌ Advertencia: Error de conexión con Langfuse. Revisa tu .env")

if os.getenv("OPENWEATHER_API_KEY"):
    print("✅ Clima: API Key de OpenWeather detectada.")
else:
    print("⚠️ Advertencia: Falta OPENWEATHER_API_KEY en el .env")
