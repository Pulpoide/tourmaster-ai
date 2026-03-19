from src.graph import run_tourmaster_graph

def run_tests():
    test_queries = [
        {"query": "¿Qué bares de rock hay en Córdoba para 200 personas?", "expected_intent": "booking"},
        {"query": "Vamos a Rosario en Kangoo, son 400km. ¿Cuánto gasto en nafta y dónde duermo?", "expected_intent": "logistics"},
        {"query": "Necesito un texto para Instagram anunciando el sold out de mañana.", "expected_intent": "marketing"},
        {"query": "¿Va a llover el sábado a la noche en el show al aire libre?", "expected_intent": "weather"},
        {"query": "¿Cuánto nos cobra La Trastienda por alquilar un viernes?", "expected_intent": "booking"},
        {"query": "Armame una gacetilla de prensa para mandar a las radios sobre nuestro nuevo disco.", "expected_intent": "marketing"},
        {"query": "¿Qué hotel en Buenos Aires nos recomiendas que tenga cochera cubierta para la camioneta?", "expected_intent": "logistics"},
        {"query": "¿Cómo va a estar el clima para la gira de la semana que viene en Mendoza?", "expected_intent": "weather"},
        {"query": "Pásame el contacto del programador de Niceto Club.", "expected_intent": "booking"},
        {"query": "Queremos hacer un festival y no sabemos si contactar a la municipalidad o a un bar, ¿qué sugieres?", "expected_intent": "booking"}
    ]

    print("🚀 Iniciando Suite de Pruebas de TourMaster AI...\n")
    aciertos = 0

    for i, test in enumerate(test_queries):
        query = test["query"]
        expected = test["expected_intent"].upper()

        print(f"--- Test #{i+1} ---")
        print(f"🗣️ Usuario: {query}")
        print(f"🎯 Intención Esperada: {expected}")

        try:
            estado_final = run_tourmaster_graph(query)
            experto_real = estado_final.get("expert_used", "DESCONOCIDO")

            if experto_real == expected:
                print(f"✅ ¡MATCH! Enrutamiento impecable hacia {experto_real}.")
                aciertos += 1
            else:
                print(f"⚠️ MISMATCH: El orquestador se confundió. Mandó a {experto_real}.")

        except Exception as e:
            print(f"❌ Error en la ejecución: {e}")

        print("\n" + "="*70 + "\n")

    print(f"📊 RESULTADO FINAL: Precisión del Orquestador: {aciertos}/{len(test_queries)}")
    print("✅ Revisa el dashboard de Langfuse para ver las trazas y las notas del Evaluador.")

if __name__ == "__main__":
    run_tests()