import sys
from src.graph import run_tourmaster_graph

def chat_interactivo():
    print("🎸 Bienvenido a TourMaster AI 🎸")
    print("Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("🗣️ Ingresa tu consulta: ")

        if user_input.lower() in ['salir', 'exit', 'quit']:
            print("¡Nos vemos en la gira! 🚐💨")
            break

        if not user_input.strip():
            continue

        try:
            estado_final = run_tourmaster_graph(user_input)
            experto_real = estado_final.get("expert_used", "DESCONOCIDO")
            respuesta = estado_final.get("answer", "No se generó respuesta.")

            print(f"\n✅ [Atendido por: {experto_real}]")
            print(f"🤖 Respuesta: {respuesta}\n")
            print("-" * 50 + "\n")

        except Exception as e:
            print(f"\n❌ Error en la ejecución: {e}\n")

def cli():
    """Punto de entrada para el comando uv run tourmaster"""
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"🗣️ Consulta: {query}")
        try:
            estado = run_tourmaster_graph(query)
            print(f"✅ [Atendido por: {estado.get('expert_used')}]")
            print(f"🤖 Respuesta: {estado.get('answer')}\n")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        chat_interactivo()

if __name__ == "__main__":
    cli()