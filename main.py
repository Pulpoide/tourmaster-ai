import sys
from src.graph import run_tourmaster_graph

def chat_interactivo():
    print("Bienvenido a Tourmaster AI")
    print("Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Ingresa tu consulta: ")

        if user_input.lower() in ['salir', 'exit', 'quit']:
            print("Nos vemos en la gira!")
            break

        if not user_input.strip():
            continue

        try:
            estado_final = run_tourmaster_graph(user_input)
            experto_real = estado_final.get("expert_used", "DESCONOCIDO")
            respuesta = estado_final.get("answer", "No se genero respuesta.")

            print(f"\n[OK] [Atendido por: {experto_real}]")
            print(f"[IA] Respuesta: {respuesta}\n")
            print("-" * 50 + "\n")

        except Exception as e:
            print(f"\n[ERROR] Error en la ejecucion: {e}\n")

def cli():
    """Punto de entrada para el comando uv run tourmaster"""
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"[CONSULTA] Consulta: {query}")
        try:
            estado = run_tourmaster_graph(query)
            print(f"[OK] [Atendido por: {estado.get('expert_used')}]")
            print(f"[IA] Respuesta: {estado.get('answer')}\n")
        except Exception as e:
            print(f"[ERROR] Error: {e}")
    else:
        chat_interactivo()

if __name__ == "__main__":
    cli()